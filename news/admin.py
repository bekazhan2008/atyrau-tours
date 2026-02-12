from django.contrib import admin
from .models import News

admin.site.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'type', 'text', 'created_at')
    list_filter = ('type')


# Register your models here.
