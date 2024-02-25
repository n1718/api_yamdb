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


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAdminUser,)


def signup(request):
    email = request.data.get('email')
    username = request.data.get('username')

    if CustomUser.objects.filter(email=email).exists():
        return Response(
            {'detail': 'Пользователь с таким email уже зарегистрирован'},
            status=status.HTTP_400_BAD_REQUEST
        )

    confirmation_code = ''.join(random.choices(
        string.ascii_letters + string.digits, k=6
    ))

    send_mail(
        'Код подтверждения',
        f'Ваш код подтверждения: {confirmation_code}',
        settings.EMAIL_HOST_USER,  # Добавить параметр в settings.py(?)
        [email],
        fail_silently=False,
    )

    user = CustomUser.objects.create_user(
        username=username, email=email, password=confirmation_code
    )
    user.save()

    return Response(
        {'detail': 'Код подтверждения отправлен на указанный email'},
        status=status.HTTP_201_CREATED
    )


# def token(request):
#     username = request.data.get('username')
#     confirmation_code = request.data.get('confirmation_code')

#     try:
#         user = CustomUser.objects.get(
#             username=username, password=confirmation_code
#         )
#     except CustomUser.DoesNotExist:
#         return Response(
#             {'detail': 'Неверное имя пользователя и/или код подтверждения'},
#             status=status.HTTP_400_BAD_REQUEST
#         )

#     ...
