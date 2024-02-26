from rest_framework import filters
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .permissions import IsOwnerOrReadOnly
from .filters import TitleFilter
from .viewsets import CreateListDestroyViewSet
from review.models import Category, Genre, Title, Review
from .serializers import (CategorySerializer,
                          GenreSerializer,
                          TitleSerializer,
                          TitleCreateSerializer,
                          ReviewSerializer, CommentSerializer)
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


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitleCreateSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly)

    def get_title(self):
        return get_object_or_404(Review, id=self.kwargs['title_id'])

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly)

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs['review_id'])

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post=self.get_review())
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
    access_token = ''
    if default_token_generator.check_token(user, generate_token(user)):
        access_token = AccessToken.for_user(user)

    return {
        'access': str(access_token),
    }
