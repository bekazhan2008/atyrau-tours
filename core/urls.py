"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from tournaments.views import home, tournaments_list, news_list
from users.views import api_login, api_register, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('tournaments/', tournaments_list, name='tournaments'),
    path('news/', news_list, name='news'),
    
    # API endpoints
    path('api/login/', api_login, name='api_login'),
    path('api/register/', api_register, name='api_register'),
    path('logout/', logout_view, name='logout'),
    
    # Auth URLs
    path('auth/', include('users.urls')),
    path('auth/', include('users.urls')),
]

if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
