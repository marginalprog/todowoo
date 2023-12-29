from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, login, authenticate
from .forms import TodoForm
from .models import Todo


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


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


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


def currenttodos(request):
    # todos = Todo.objects.all() - Отображает все записи из БД
    todos = Todo.objects.filter(user=request.user, date_deadline__isnull=True)
    return render(request, 'todo/currenttodos.html', {'todos': todos})
