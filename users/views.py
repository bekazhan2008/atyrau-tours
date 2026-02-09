import json
from django.http import JsonResponse
from django.contrib.auth import login, logout
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.shortcuts import redirect
from .models import User
from .tokens import account_activation_token


@require_http_methods(["POST"])
def api_register(request):
    try:
        data = json.loads(request.body)
        username = data.get('login')
        email = data.get('email')
        password = data.get('password')

        if User.objects.filter(username=username).exists():
            return JsonResponse({'success': False, 'message': 'Username already exists'}, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'message': 'Email already exists'}, status=400)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active=False
        )

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)

        activation_link = request.build_absolute_uri(
            reverse('activate', kwargs={'uidb64': uid, 'token': token})
        )

        send_mail(
            'Подтверждение аккаунта',
            f'Нажми на ссылку для активации:\n{activation_link}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        return JsonResponse({
            'success': True,
            'message': 'Check your email to activate account'
        })

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('home')
        else:
            return JsonResponse({'success': False, 'message': 'Activation link invalid'})

    except:
        return JsonResponse({'success': False, 'message': 'Activation failed'})


@require_http_methods(["POST"])
def api_login(request):
    from django.contrib.auth import authenticate

    data = json.loads(request.body)
    login_input = data.get('login')
    password = data.get('password')

    user = authenticate(request, username=login_input, password=password)

    if user is not None:
        if not user.is_active:
            return JsonResponse({'success': False, 'message': 'Account not activated'}, status=403)

        login(request, user)
        return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'message': 'Invalid credentials'}, status=401)


def logout_view(request):
    logout(request)
    return redirect('home')