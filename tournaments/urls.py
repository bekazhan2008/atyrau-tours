from django.urls import path
from . import views

app_name = 'tournaments'

urlpatterns = [
    path('tournaments/', views.tournaments_list, name='list'),
]

app_name = 'news'

urlpatterns += [
    path('', views.news_list, name='news'),
]