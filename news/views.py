from django.shortcuts import render
from .models import News, MainNews

def news(request):
    news = News.objects.all()
    main_news = MainNews.objects.filter(is_published=True).order_by('-created_at').first()
    return render(request, 'news/news.html', {'news': news, 'main_news': main_news})

