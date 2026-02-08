from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .forms import LoginForm, RegisterForm
from .models import User
import json
from django.http import JsonResponse
from django.contrib import messages


def home(request):
    login_form = LoginForm()
    return render(request, 'users/home.html', {'login_form': login_form})

def register_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        username = request.POST.get("nickname")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password != password2:
            return redirect("home")

        if User.objects.filter(username=username).exists():
            return redirect("home")

        if User.objects.filter(email=email).exists():
            return redirect("home")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)
        return redirect("home")

    return redirect("home")

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                form.add_error(None, 'Неверный логин или пароль')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

def api_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")

        return redirect("home")

def logout_view(request):
    """Logout user"""
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    """User profile page"""
    return render(request, 'users/profile.html', {'user': request.user})