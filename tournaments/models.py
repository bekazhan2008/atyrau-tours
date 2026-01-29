from django.db import models

# Create your models here.

#Запись игр: КС2, Дота 2, Валик
class Game(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

#Место проведения
class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.name

#Сами турики + добавление в таблицу и удаление всех туриков по определенной игре при удалении самой игры
class Tournament(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE
    )

    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE
    )

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    max_participants = models.PositiveIntegerField()
    created_at = models.DateTimeField()

    def __str__(self):
        return self.title