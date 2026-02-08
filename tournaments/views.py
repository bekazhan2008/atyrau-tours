from django.shortcuts import render
from .models import Tournament, PastTournament

def home(request):
    active_tournament = Tournament.objects.filter(is_active=True).first()
    tournaments = Tournament.objects.exclude(is_active=True).order_by('-start_date')[:6]
    
    context = {
        'active_tournament': active_tournament,
        'tournaments': tournaments,
    }
    return render(request, 'home.html', context)

def tournaments_list(request):
    active_tournament = Tournament.objects.filter(is_active=True).first()
    tournaments = Tournament.objects.filter(is_active=False).order_by('-start_date')
    past_tournaments = PastTournament.objects.all()
    
    # Filter by game if provided
    game = request.GET.get('game')
    if game and game != 'all':
        tournaments = tournaments.filter(game=game)
    
    context = {
        'active_tournament': active_tournament,
        'tournaments': tournaments,
        'past_tournaments': past_tournaments,
    }
    return render(request, 'tournaments.html', context)

def news_list(request):
    return render(request, 'news.html')