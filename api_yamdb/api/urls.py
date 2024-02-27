from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import SignUp, GetToken, MeViewSet, CustomUserViewSet

router_v1 = DefaultRouter()
router_v1.register(r'users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', SignUp.as_view(), name='signup'),
    path('v1/auth/token/', GetToken.as_view(), name='token'),
    path('v1/users/me/', MeViewSet, name='me'),
]
