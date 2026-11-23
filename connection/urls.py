
from django.urls import path #type: ignore
from rest_framework_simplejwt.views import TokenRefreshView #type: ignore

from .views import (RegisterView,LoginView,ProfileView,LogoutView)

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/me/", ProfileView.as_view(), name="profile"),
]
