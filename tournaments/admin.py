from django.contrib import admin
from .models import Game, Location, Tournament

# Register your models here.

admin.site.register(Game)
admin.site.register(Location)
admin.site.register(Tournament)