from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet, signup  # Описать CustomUserViewSet в views.py

router_v1 = DefaultRouter()
router_v1.register(r'users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('auth/', include('djoser.urls')),  # Авторизация через Djoser, потом нужно будет переделать
    path('/v1/auth/signup/', signup())
]
