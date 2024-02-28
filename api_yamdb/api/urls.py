from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

from .views import (
    TitleViewSet,
    CategoryViewSet,
    GenreViewSet,
    ReviewViewSet,
    CommentViewSet,
    SignUp,
    GetToken,
    MeViewSet,
    CustomUserViewSet
)

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register(r'users', views.CustomUserViewSet, basename='users')
router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(r'genres', GenreViewSet, basename='genres')
router_v1.register(
    r'titles/(?P<title_id>[\d]+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>[\d]+)/reviews/(?P<review_id>[\d]+)/comments/',
    CommentViewSet,
    basename='comments')
router_v1.register(r'users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', SignUp.as_view(), name='signup'),
    path('v1/auth/token/', GetToken.as_view(), name='token'),
    path('v1/users/me/', MeViewSet, name='me'),
]
