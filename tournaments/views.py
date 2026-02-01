from django.shortcuts import render
from .models import Tournament, PastTournament

def tournaments_list(request):
    active_tournament = Tournament.objects.filter(is_active=True).first()
    tournaments = Tournament.objects.exclude(is_active=True).order_by('-start_date')
    past_tournaments = PastTournament.objects.all()
    
    context = {
        'active_tournament': active_tournament,
        'tournaments': tournaments,
        'past_tournaments': past_tournaments,
    }
    return render(request, 'tournaments.html', context)

def news_list(request):
    return render(request, 'news.html')