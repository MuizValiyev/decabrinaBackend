from django.urls import path
from .views import EmailCheckAPIView, LoginAPIView, RegisterAPIView, PasswordResetConfirmAPIView, PasswordResetRequestAPIView
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('check-email/', EmailCheckAPIView.as_view(), name='check-email'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password-reset/', PasswordResetRequestAPIView.as_view(), name='password-reset'),
    path('password-reset/confirm/', PasswordResetConfirmAPIView.as_view(), name='password-reset-confirm'),
]

urlpatterns += [
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
