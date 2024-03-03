from rest_framework import filters
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, generics
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated
)
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

from .permissions import IsOwnerOrReadOnly, IsSuperUser
from .filters import TitleFilter
from .viewsets import CreateListDestroyViewSet
from review.models import Category, Genre, Title, Review, CustomUser
from .serializers import (CategorySerializer,
                          GenreSerializer,
                          TitleSerializer,
                          TitleCreateSerializer,
                          ReviewSerializer,
                          CommentSerializer,
                          SignUpSerializer,
                          TokenSerializer,
                          CustomUserSerializer,
                          CustomUserUpdateSerializer)


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = (IsAuthenticated, IsSuperUser)
    pagination_class = PageNumberPagination  # Недонастроил до конца,
    # не могу выкупить, как можно получить параметр count из пагинатора

    @action(
        methods=['get', 'patch', ], detail=False,
        url_path='me', url_name='me',
        permission_classes=(IsAuthenticated,),
    )
    def owner_profile(self, request):
        user = request.user
        if request.method == 'PATCH':
            serializer = CustomUserUpdateSerializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
            user.confirmation_code = confirmation_code
            user.save()

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
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            user = get_object_or_404(CustomUser, username=username)
            token = AccessToken.for_user(user)
            token['payload'] = user.role

            return Response(
                {'token': str(token)},
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
