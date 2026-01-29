from django.urls import path
from .views import tournament_list

app_name = 'tournaments'

urlpatterns = [
    path('', tournament_list, name='list')
]