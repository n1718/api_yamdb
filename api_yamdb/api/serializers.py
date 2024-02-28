from rest_framework import serializers
from django.utils import timezone
from django.db.models import Avg
from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from review.models import Genre, Category, Title, Review, Comment, CustomUser


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class TitleSerializer(serializers.ModelSerializer):

    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        rating = obj.reviews.aggregate(Avg('score')).get('score__avg')
        return rating if not rating else round(rating, 0)

    class Meta:
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category')
        model = Title


class TitleCreateSerializer(serializers.ModelSerializer):

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category')
        model = Title

        def validate_year(self, value):
            year_now = timezone.now.year
            if value <= 0 or value > year_now:
                raise serializers.ValidationError(
                    'Год создания должен быть нашей эры и не больше текущего.'
                )
            return value


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'author', 'text', 'score', 'pub_date', 'title')
        model = Review
        read_only_fields = ('title',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'author', 'text', 'created', 'review')
        model = Comment
        read_only_fields = ('review',)
        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['author', 'title']
            )
        ]


class CustomUserSerializer(serializers.ModelSerializer):
    validators = [
        RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Введите корректное имя пользователя',
            code='invalid_username'
        )
    ]

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        ]

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать "me" в качестве имени пользователя'
            )
        return value

    def validate_user_role_choice(self, data):
        user = self.context['request'].user

        if user.is_staff:
            return data

        data['role'] = 'user'
        return data


class SignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('username', 'email',)

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать "me" в качестве имени пользователя'
            )
        return value


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        confirmation_code = data.get('confirmation_code')

        if not username or not confirmation_code:
            raise serializers.ValidationError(
                'Обязательные для валидации поля отсутствуют'
            )

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            serializers.ValidationError('Пользователь не существует')

        if user.confirmation_code != confirmation_code:
            raise serializers.ValidationError('Неверный код подтверждения')

        return data

    class Meta:
        model = CustomUser
        fields = ('username', 'confirmation_code')


class MeSerializer(serializers.ModelSerializer):
    ...  # Изменение данных своего профиля
