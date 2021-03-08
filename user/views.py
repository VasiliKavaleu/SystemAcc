from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.contrib import messages

from . forms import SignUpForm, LoginForm


def register(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            login_user = authenticate(request,
                                      email=request.POST['email'],
                                      password=request.POST['password1']
                                      )
            if login_user is not None:
                login(request, login_user)
            messages.success(request, 'Вы успешно зарегистрированы!')
            return redirect('user:register')
        else:
            return render(request, 'register.html', {'form': form})
    return render(request, 'register.html', {'form': form})


def login_user(request):
    form = LoginForm()
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('main:main_page')
        else:
            messages.info(request, 'Нет такого пользователя! '
                                   'Проверьте введенные данные.')
            return redirect('user:login_user')
    else:
        return render(request, 'login_user.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('main:main_page')
