from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.views import OTPRequestAPIView, UserListCreateAPIView


urlpatterns = [
    path("users/", UserListCreateAPIView.as_view(), name="user-list-create"),
    path("otp/request/", OTPRequestAPIView.as_view(), name="otp-request"),
    path("jwt/token/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]
