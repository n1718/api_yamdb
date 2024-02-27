from django.core.validators import RegexValidator
from rest_framework import serializers
from review.models import CustomUser
from django.db import models


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
    ...  # Обрабатывает получение JWT-токена и confirmition-code
    confirmation_code = models.CharField()

    class Meta:
        model = CustomUser
        fields = ('username', 'confirmation_code')


class MeSerializer(serializers.ModelSerializer):
    ...  # Изменение данных своего профиля
