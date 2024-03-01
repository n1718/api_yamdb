from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser

from .validators import validate_year


ROLE_CHOICES = [
    ('user', 'User'),
    ('moderator', 'Moderator'),
    ('admin', 'Admin'),
]


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True, max_length=254, blank=False,)
    bio = models.TextField(null=True, blank=True)
    role = models.CharField(
        default='user', choices=ROLE_CHOICES, max_length=150
    )
    confirmation_code = models.CharField(max_length=150)


class Category(models.Model):
    """Категории произведений."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Слаг категории'
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    """Жанры произведений."""

    name = models.CharField(
        max_length=256,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг жанра'
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Произведения."""
    name = models.CharField(
        max_length=100,
        verbose_name='Название произведения'
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год создания',
        validators=[
            MinValueValidator(0),
            validate_year]
    )
    description = models.TextField(
        verbose_name='Описание произведения',
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='genre',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='category',
        verbose_name='Категория',
    )


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField()
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True)


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="comments")
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True)
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE
    )

    def __str__(self) -> str:
        return self.genre

