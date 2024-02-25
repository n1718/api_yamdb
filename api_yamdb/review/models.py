from django.db import models
from django.contrib.auth.models import AbstractUser

ROLE_CHOICES = [
    ('user', 'User'),
    ('moderator', 'Moderator'),
    ('admin', 'Admin'),
]


class CustomUser(AbstractUser):
    username = models.CharField(unique=True, max_length=150, blank=False,)
    email = models.EmailField(unique=True, max_length=254, blank=False,)
    first_name = models.TextField(max_length=150,)
    last_name = models.TextField(max_length=150,)
    bio = models.TextField()
    role = models.CharField(
        default='user', choices=ROLE_CHOICES, max_length=150
    )

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_groups',
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_user_permissions',
        blank=True,
    )
