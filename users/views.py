from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .forms import LoginForm, RegisterForm
from .models import User
from tournaments.models import Tournament, PastTournament
import json
from django.http import JsonResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator


def home(request):
    tournaments = Tournament.objects.all()
    login_form = LoginForm()
    return render(request, 'users/home.html', {'login_form': login_form, 'tournaments': tournaments})


def register_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        username = request.POST.get("nickname")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        if password != password2:
            messages.error(request, "Пароли не совпадают")
            return redirect("home")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Такой логин уже существует")
            return redirect("home")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Такая почта уже используется")
            return redirect("home")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active=False  # Пользователь не активен до подтверждения
        )

        # Отправка письма с подтверждением
        current_site = get_current_site(request)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        link = f"http://{current_site.domain}/activate/{uid}/{token}/"

        send_mail(
            subject="Подтверждение регистрации",
            message=f"Привет {username}! Подтверди регистрацию по ссылке:\n{link}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False,
        )

        messages.success(request, "Письмо с подтверждением отправлено на вашу почту!")
        return redirect("home")

    return redirect("home")


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        user.save()
        login(request, user)
        messages.success(request, "Почта подтверждена! Вы вошли в систему.")
        return redirect("home")
    else:
        messages.error(request, "Ссылка недействительна или устарела.")
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

@login_required
def update_profile(request):
    if request.method == 'POST':
        user = request.user
        # Обновляем ник
        user.username = request.POST.get('username')
        
        # Обработка аватарки
        if 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']
            
        user.save()
    return redirect('profile')