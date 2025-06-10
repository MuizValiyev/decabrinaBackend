from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .models import CustomUser, OTPSession
from .serializers import (RegisterSerializer, LoginSerializer, EmailCheckSerializer, OTPSessionCreateSerializer, OTPVerifySerializer, NewPasswordSerializer)
from rest_framework_simplejwt.tokens import RefreshToken


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
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            return Response({
                'message': 'User registered',
                'user_id': user.id,
                'tokens': tokens
            }, status=201)
        return Response(serializer.errors, status=400)


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(request, email=email, password=password)

        if not user:
            return Response({'error': 'Invalid credentials'}, status=401)

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
        return Response({'session_id': session.session_id}, status=201)


class OTPVerifyAPIView(GenericAPIView):
    serializer_class = OTPVerifySerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({
            'message': 'Код успешно подтверждён',
            'email': serializer.validated_data['email']
        }, status=200)


class NewPasswordAPIView(GenericAPIView):
    serializer_class = NewPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Пароль успешно обновлён"}, status=200)
