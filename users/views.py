from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from .models import CustomUser, OTPSession
from .serializers import (
    RegisterSerializer, LoginSerializer, EmailCheckSerializer,
    OTPSessionCreateSerializer, OTPVerifySerializer, NewPasswordSerializer, UserIDSerializer
)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': f'Bearer {str(refresh)}',
        'access': f'Bearer {str(refresh.access_token)}',
    }


class EmailCheckAPIView(GenericAPIView):
    serializer_class = EmailCheckSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        exists = CustomUser.objects.filter(email=email).exists()
        return Response({'registered': exists})


class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        tokens = get_tokens_for_user(user)
        return Response({
            'message': 'User registered',
            'user_id': user.id,
            'tokens': tokens
        }, status=status.HTTP_201_CREATED)


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(request, email=email, password=password)

        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        tokens = get_tokens_for_user(user)
        return Response({
            'message': 'Login successful',
            'user_id': user.id,
            'tokens': tokens
        })


class OTPSessionCreateAPIView(GenericAPIView):
    serializer_class = OTPSessionCreateSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        session = serializer.save()
        return Response({'session_id': session.session_id}, status=status.HTTP_201_CREATED)


class OTPVerifyAPIView(GenericAPIView):
    serializer_class = OTPVerifySerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({
            'message': 'Код успешно подтверждён',
            'email': serializer.validated_data['email']
        }, status=status.HTTP_200_OK)


class NewPasswordAPIView(GenericAPIView):
    serializer_class = NewPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Пароль успешно обновлён"}, status=status.HTTP_200_OK)


class UserIDAPIView(GenericAPIView):
    serializer_class = UserIDSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = {"user_id": request.user.id}
        serializer = self.get_serializer(data)
        return Response(serializer.data)
