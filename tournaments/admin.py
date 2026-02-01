from django.contrib import admin
from .models import Tournament, PastTournament

@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'game', 'status', 'prize_pool', 'start_date')
    list_filter = ('status', 'game')
    search_fields = ('name', 'game')

@admin.register(PastTournament)
class PastTournamentAdmin(admin.ModelAdmin):
    list_display = ('name', 'winner', 'prize_pool', 'completion_date')