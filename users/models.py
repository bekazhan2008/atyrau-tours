from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('player', 'Участник'),
        ('organizer', 'Организатор'),
        ('admin', 'Админ'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='player')
    city = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    email = models.CharField(max_length=100, blank=False, null=False, default='default@example.com')

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

