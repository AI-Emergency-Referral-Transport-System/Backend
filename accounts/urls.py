from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.views import (
    AuthRootAPIView,
    OTPRequestAPIView, 
    OTPVerifyAPIView, 
    ProfileRetrieveUpdateAPIView
)

# It is good practice to define an app_name for namespacing
app_name = "accounts"

urlpatterns = [
    path("", AuthRootAPIView.as_view(), name="auth-root"),
    # Primary auth endpoints
    path("signup/", OTPRequestAPIView.as_view(), name="signup"),
    path("otp/request/", OTPRequestAPIView.as_view(), name="otp-request-clean"),
    path("otp/verify/", OTPVerifyAPIView.as_view(), name="otp-verify-clean"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh-clean"),
    
    # Legacy auth-prefixed endpoints kept for compatibility
    path("auth/otp/request/", OTPRequestAPIView.as_view(), name="otp-request"),
    path("auth/otp/verify/", OTPVerifyAPIView.as_view(), name="otp-verify"),
    
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    
    # User Profile Endpoints
    path("profile/", ProfileRetrieveUpdateAPIView.as_view(), name="profile-detail"),
]
