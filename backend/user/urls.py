from django.urls import path

from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    RegisterView,
    ProfileView,
    CustomTokenObtainPairView,
    OTPRequestView,
    PasswordResetView,
)


app_name = "user"

urlpatterns = [
    # Authentication flow
    path("access/", CustomTokenObtainPairView.as_view(), name='access'),
    path("register/", RegisterView.as_view(), name='register'),
    path("profile/", ProfileView.as_view(), name='profile'),
    path("refresh/", TokenRefreshView.as_view(), name='refresh'),

    # Password reset flow
    path("otp/request/", OTPRequestView.as_view(), name='otp'),
    path("password/reset/", PasswordResetView.as_view(), name='reset'),
]
