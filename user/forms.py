from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class SignUpForm(UserCreationForm):
    name = forms.CharField(max_length=254, label='Имя', widget=forms.TextInput(
        attrs={'class': 'form-control'}
    ))
    email = forms.EmailField(max_length=254, label='Email адрес',
                             help_text='Это поле обязательно',
                             widget=forms.TextInput(
                                 attrs={'class': 'form-control'}
                             ))
    password1 = forms.CharField(max_length=254, label='Пароль',
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control'}
                                ))
    password2 = forms.CharField(max_length=254, label='Подтвердите пароль',
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control'}
                                ))

    class Meta:
        model = User
        fields = ('name', 'email', 'password1', 'password2')


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=254, help_text='Это поле обязательно',
                             widget=forms.TextInput(
                                 attrs={'class': 'form-control'}
                             ))
    password = forms.CharField(max_length=254, widget=forms.PasswordInput(
        attrs={'class': 'form-control'}
    ))
