from django.shortcuts import render
from .models import Tournament

# Create your views here.

def tournament_list(request):
    tournaments = Tournament.objects.select_related('game', 'location')
    return render(request, 'tournament_list.html', {
        'tournaments': tournaments
    })