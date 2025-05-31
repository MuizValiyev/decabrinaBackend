from django.urls import path
from .views import EmailCheckAPIView, LoginAPIView, RegisterAPIView

urlpatterns = [
    path('check-email/', EmailCheckAPIView.as_view(), name='check-email'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('register/', RegisterAPIView.as_view(), name='register'),
]
