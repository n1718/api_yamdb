from django.db.models import Avg
from django.utils import timezone
from rest_framework import serializers

from reviews.models import Category, Comment, CustomUser, Genre, Review, Title

from .utils import validate_email, validate_name


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
        fields = ('id', 'author', 'text', 'score', 'pub_date')
        model = Review

    def validate(self, data):
        if not self.context.get('request').method == 'POST':
            return data
        author = self.context.get('request').user
        title_id = self.context.get('view').kwargs.get('title_id')
        if Review.objects.filter(author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'Можно оставить только один отзыв на произведение!'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date')
        model = Comment


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:

        model = CustomUser
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role',)
        read_only_fields = (
            'id', 'password', 'last_login', 'is_superuser', 'is_staff',
            'is_active', 'date_joined', 'confirmation_code',
            'groups', 'user_permissions'
        )


class CustomUserUpdateSerializer(serializers.ModelSerializer):

    class Meta:

        model = CustomUser
        fields = ('first_name', 'last_name', 'bio', 'username', 'email',)
        read_only_fields = (
            'id', 'password', 'last_login', 'is_superuser', 'is_staff',
            'is_active', 'date_joined', 'role', 'confirmation_code',
            'is_email_confirmed', 'confirmation_code_created_at',
            'groups', 'user_permissions'
        )

    def validate_username(self, value):
        """Validate the username field."""
        validate_name(value)
        return value

    def validate_email(self, value):
        """Validate the email field."""
        validate_email(value)
        return value


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
            if user.confirmation_code != confirmation_code:
                raise serializers.ValidationError('Неверный код подтверждения')
        except CustomUser.DoesNotExist:
            serializers.ValidationError('Пользователь не существует')

        return data

    class Meta:
        model = CustomUser
        fields = ('username', 'confirmation_code')
