from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from review.models import CustomUser
from .serializers import CustomUserSerializer
from django.core.mail import send_mail
from django.conf import settings
import random
import string
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAdminUser,)


# def signup(request):
#     email = request.data.get('email')
#     username = request.data.get('username')

#     if CustomUser.objects.filter(email=email).exists():
#         return Response(
#             {'detail': 'Пользователь с таким email уже зарегистрирован'},
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     # confirmation_code = ''.join(random.choices(
#     #     string.ascii_letters + string.digits, k=6
#     # ))  # Ручная генерация кода подтверждения

#     token = default_token_generator.make_token(request.user)

#     send_mail(
#         'Код подтверждения',
#         f'Ваш код подтверждения: {confirmation_code}',
#         settings.EMAIL_HOST_USER,  # Добавить параметр в settings.py(?)
#         [email],
#         fail_silently=False,
#     )

#     user = CustomUser.objects.create_user(
#         username=username, email=email, password=confirmation_code
#     )
#     user.save()

#     return Response(
#         {'detail': 'Код подтверждения отправлен на указанный email'},
#         status=status.HTTP_201_CREATED
#     )

#     return token


def generate_token(user):
    token = default_token_generator.make_token(user)
    return token


def get_tokens_for_user(user):
    if default_token_generator.check_token(user, generate_token()):
        access_token = AccessToken.for_user(user)

    return {
        'access': str(access_token),
    }
