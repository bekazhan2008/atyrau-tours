from django.db import models

# Create your models here.
class News(models.Model):
    title = models.CharField("Заголовок", max_length=200)
    text = models.TextField("Текст новости")
    created_at = models.DateTimeField("Дата публикации", auto_now_add=True)
    is_published = models.BooleanField("Опубликовано", default=True)

    def __str__(self):
        return self.title

