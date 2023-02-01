from django.urls import path, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    UserView,
    UpdatePasswordView,
    AdminUsersView,
    CustomTokenObtainPairView
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('register/', RegisterView.as_view(), name='register_user'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login_user'),
    # path('user/login/', LoginView.as_view(), name='login_user'),
    path('logout/', LogoutView.as_view(), name='logout_user'),
    path('profile/', UserView.as_view(), name='user_details'),
    path('reset/', UpdatePasswordView.as_view(), name='user_password'),
    path('all/', AdminUsersView.as_view(), name='admin-users-all'),
]
