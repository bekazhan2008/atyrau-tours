from django.db import models

# Create your models here.
class News(models.Model):
    TYPE_CHOISES = [
        ('tournaments', 'Турниры'),
        ('teams', 'Команды'),
        ('updates', 'Обновления'),
        ('patches', 'Патчи'),
    ]

    title = models.CharField("Заголовок", max_length=200)
    img = models.ImageField("Изображение", upload_to='static/img/', null=True, blank=True)
    type = models.CharField("Тип новости", max_length=50, choices=TYPE_CHOISES)
    text = models.TextField("Текст новости")
    created_at = models.DateTimeField("Дата публикации", auto_now_add=True)
    is_published = models.BooleanField("Опубликовано", default=True)

    def __str__(self):
        return self.title

class MainNews(models.Model):
    title = models.CharField("Заголовок", max_length=200)
    img = models.ImageField("Изображение", upload_to='static/img/', null=True, blank=True)
    text = models.TextField("Текст новости")
    created_at = models.DateTimeField("Дата публикации", auto_now_add=True)
    is_published = models.BooleanField("Опубликовано", default=True)

    def __str__(self):
        return self.title