from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import status, viewsets, generics
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from review.models import CustomUser
from .serializers import (
    CustomUserSerializer, SignUpSerializer, TokenSerializer
)


class SignUp(generics.CreateAPIView):
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        username = request.data.get('username')
        email = request.data.get('email')
        user = CustomUser.objects.filter(
            username=username, email=email
        ).exists()

        if serializer.is_valid() or user:
            user, created = CustomUser.objects.get_or_create(
                username=username, email=email
            )
            confirmation_code = default_token_generator.make_token(user)
            send_mail(
                'Код подтверждения',
                f'Ваш код подтверждения: {confirmation_code}',
                'example@email.com',
                [email],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetToken(generics.CreateAPIView):
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        user = get_object_or_404(CustomUser, username=username)

        if default_token_generator.check_token(user, confirmation_code):
            return Response(
                {'token': str(AccessToken.for_user(user))},
                status=status.HTTP_200_OK
            )

        return Response(
            {'confirmation_code': 'Неверный код подтверждения'},
            status=status.HTTP_400_BAD_REQUEST
        )


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAdminUser,)


class MeViewSet(viewsets.ModelViewSet):
    ...
