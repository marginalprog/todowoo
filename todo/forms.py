# from django.contrib.auth.models import User
from django.conf import settings
from django.forms import ModelForm
from django import forms
from .models import Todo, CustomUser


class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description', 'important']


class UserForm(ModelForm):
    birth_date = forms.DateField(widget=forms.DateInput(format='%d.%m.%Y'), input_formats=['%d.%m.%Y'])

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'bio', 'location', 'birth_date')  # ++


"""
class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('location', 'birth_date')
"""