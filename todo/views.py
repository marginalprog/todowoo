from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, login, authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'todo/home.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')  # !!! Перенаправление на ниже созданное отображение
            except IntegrityError:
                return render(request, 'todo/signupuser.html',
                              {'form': UserCreationForm(), 'error': 'Данное имя пользователя занято'})

        else:
            return render(request, 'todo/signupuser.html',
                          {'form': UserCreationForm(), 'error': 'Несовпадение паролей'})
            # Уведомление о неправильном пароле


def loginuser(request):
    if request.method == 'GET':  # Если приходит гет-запрос, то перенаправляем пользователя на логин
        return render(request, 'todo/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo/loginuser.html',
                          {'form': AuthenticationForm(), 'error': 'Некорректный пароль пользователя'})
        else:
            login(request, user)
            return redirect('currenttodos')  # !!! Перенаправление на ниже созданное отображение


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


@login_required
def createtodo(request):
    if request.method == 'GET':  # Если пользователь зашел на страницу - отображаем форму
        return render(request, 'todo/createtodo.html', {'form': TodoForm()})
    else:  # Если пользователь отправляет данные
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form': TodoForm(), 'error': 'Введены некорректные данные'})


@login_required
def currenttodos(request):
    # todos = Todo.objects.all() - Отображает все записи из БД
    todos = Todo.objects.filter(user=request.user, date_deadline__isnull=True)
    return render(request, 'todo/currenttodos.html', {'todos': todos})


@login_required
def completedtodos(request):
    # todos = Todo.objects.all() - Отображает все записи из БД
    todos = Todo.objects.filter(user=request.user, date_deadline__isnull=False).order_by('-date_deadline')
    return render(request, 'todo/completedtodos.html', {'todos': todos})


@login_required
def viewtodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)  # !!!
    # Todo.objects.filter(user=request.user)
    # formatDate = created_date.strftime("%d/%m/%Y")
    if request.method == 'GET':  # Отображение формы изменения записи
        form = TodoForm(instance=todo)  # параметр для работы с уже существующим объектом
        return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form})
    else:  # Отправка изменений
        try:
            form = TodoForm(request.POST, instance=todo)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo': todo, 'form': form, 'error': 'Некорректные данные'})


@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.date_deadline = timezone.now()
        todo.save()
        return redirect('currenttodos')


@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')
