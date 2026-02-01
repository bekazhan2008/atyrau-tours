from django.db import models

# Create your models here.

class Tournament(models.Model):
    STATUS_CHOICES = [
        ('registration', 'Открыта регистрация'),
        ('upcoming', 'Скоро'),
        ('completed', 'Завершён'),
    ]

    FORMAT_CHOICES = [
        ('single_elim', 'Single Elimination'),
        ('double_elim', 'Double Elimination'),
        ('swiss', 'Swiss System'),
        ('round_robin', 'Round Robin'),
    ]

    name = models.CharField(max_length=255, verbose_name='Название турнира')
    game = models.CharField(max_length=255, verbose_name='Игра')
    region = models.CharField(max_length=255, verbose_name='Регион')
    prize_pool = models.CharField(max_length=50, verbose_name='Призовой фонд')
    start_date = models.DateTimeField(verbose_name='Дата и время начала')
    max_teams = models.PositiveIntegerField(default=16, verbose_name='Максимальное количество команд')
    registred_teams = models.PositiveIntegerField(default=0, verbose_name='Зарегистрированные команды')
    format = models.CharField(max_length=20, choices=FORMAT_CHOICES, default='single_elim', verbose_name='Формат турнира')
    location = models.CharField(max_length=255, verbose_name='Место проведения')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='registration', verbose_name='Статус турнира')
    is_active = models.BooleanField(default=False, verbose_name='Активен')

    class Meta:
        ordering  = ['-start_date']

    def __str__(self):
        return self.name
    
class PastTournament(models.Model):
    name = models.CharField(max_length=200)
    winner = models.CharField(max_length=200)
    prize_pool = models.CharField(max_length=50)
    completion_date = models.DateField()
    teams_count = models.IntegerField()
    
    class Meta:
        ordering = ['-completion_date']
    
    def __str__(self):
        return self.name