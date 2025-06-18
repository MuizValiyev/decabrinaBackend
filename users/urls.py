from django.urls import path
from .views import EmailCheckAPIView, LoginAPIView, RegisterAPIView, OTPSessionCreateAPIView, OTPVerifyAPIView, NewPasswordAPIView, UserIDAPIView
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

urlpatterns = [
    path('check-email/', EmailCheckAPIView.as_view(), name='check-email'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password-reset/', OTPSessionCreateAPIView.as_view(), name='password-reset'),
    path('password-reset/confirm/', OTPVerifyAPIView.as_view(), name='password-reset-confirm'),
    path('new-password/', NewPasswordAPIView.as_view(), name='new-password'),
    path('me/', UserIDAPIView.as_view(), name='user-id'),
]

urlpatterns += [
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
