from django.db import models
from django.contrib.auth.models import AbstractUser

ROLE_CHOICES = [
    ('user', 'User'),
    ('moderator', 'Moderator'),
    ('admin', 'Admin'),
]


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, max_length=254, blank=False,)
    bio = models.TextField()
    role = models.CharField(
        default='user', choices=ROLE_CHOICES, max_length=150
    )
