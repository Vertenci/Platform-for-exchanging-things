from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from django.contrib.auth import login, logout
from django.contrib import messages


def clogin(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('ads_list')
        else:
            messages.error(request, "Неверные данные для входа")
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def registration(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ads_list')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})


def clogout(request):
    logout(request)
    return redirect('login')
