from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .forms import LoginForm, RegisterForm
from .models import User
from django.contrib import messages
import json
from django.http import JsonResponse


def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'users/home.html')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Аккаунт {user.username} успешно создан!')
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})

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
    return redirect('login')

@require_http_methods(["POST"])
def api_login(request):
    """API endpoint for login"""
    try:
        data = json.loads(request.body)
        login_input = data.get('login')
        password = data.get('password')
        
        # Try to authenticate by username or email
        user = authenticate(request, username=login_input, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({
                'success': True,
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Invalid credentials'
            }, status=401)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)

@require_http_methods(["POST"])
def api_register(request):
    """API endpoint for registration"""
    try:
        data = json.loads(request.body)
        username = data.get('login')
        email = data.get('email')
        password = data.get('password')
        phone = data.get('phone', '')
        
        # Validation
        if User.objects.filter(username=username).exists():
            return JsonResponse({
                'success': False,
                'message': 'Username already exists'
            }, status=400)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({
                'success': False,
                'message': 'Email already exists'
            }, status=400)
        
        if len(password) < 6:
            return JsonResponse({
                'success': False,
                'message': 'Password must be at least 6 characters'
            }, status=400)
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            phone=phone
        )
        
        login(request, user)
        
        return JsonResponse({
            'success': True,
            'message': 'Registration successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }
        })
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)

def logout_view(request):
    """Logout user"""
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    """User profile page"""
    return render(request, 'users/profile.html', {'user': request.user})