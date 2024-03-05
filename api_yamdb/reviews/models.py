from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .validators import validate_year
from api_yamdb import settings

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
        max_length=settings.MAX_LENGTH_NAME,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        unique=True,
        max_length=settings.MAX_LENGTH_SLUG,
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
        max_length=settings.MAX_LENGTH_NAME,
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        max_length=settings.MAX_LENGTH_SLUG,
        unique=True,
        verbose_name='Слаг жанра'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self) -> str:
        return self.name


class Title(models.Model):
    """Произведения."""

    name = models.CharField(
        max_length=settings.MAX_LENGTH_NAME,
        verbose_name='Название произведения'
    )
    year = models.SmallIntegerField(
        verbose_name='Год создания',
        validators=[validate_year]
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
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                settings.REVIEW_SCORE_MIN_VALUE,
                message='Оценка имеет границы от 1 до 10'
            ),
            MaxValueValidator(
                settings.REVIEW_SCORE_MAX_VALUE,
                message='Оценка имеет границы от 1 до 10'
            ),
        ]
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_pair'
            ),
        ]
        ordering = ('pub_date',)
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'


class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="comments")
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True)
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta:
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'


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
