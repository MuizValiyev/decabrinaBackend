import random
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .models import CustomUser, PasswordResetCode
from .serializers import RegisterSerializer, LoginSerializer, EmailCheckSerializer, PasswordResetConfirmSerializer, PasswordResetRequestSerializer
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class EmailCheckAPIView(GenericAPIView):
    serializer_class = EmailCheckSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        email = serializer.validated_data['email']
        exists = CustomUser.objects.filter(email=email).exists()
        return Response({'registered': exists})


class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(request, email=email, password=password)
        if user is None:
            return Response({'error': 'Invalid credentials'}, status=401)

        tokens = get_tokens_for_user(user)
        return Response({
            'message': 'Login successful',
            'user_id': user.id,
            'tokens': tokens
        })


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
    

class PasswordResetRequestAPIView(GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']

        if not CustomUser.objects.filter(email=email).exists():
            return Response({'error': 'Пользователь с таким email не найден'}, status=404)

        recent = PasswordResetCode.objects.filter(email=email).order_by('-created_at').first()
        if recent and timezone.now() - recent.created_at < timedelta(seconds=60):
            return Response({'error': 'Подождите перед повторной отправкой'}, status=429)

        code = f"{random.randint(100000, 999999)}"
        PasswordResetCode.objects.create(email=email, code=code)

        send_mail(
            'Сброс пароля',
            f'Ваш код сброса пароля: {code}',
            'noreply@yourdomain.com',
            [email],
            fail_silently=False
        )

        return Response({'message': 'Код сброса отправлен на почту'}, status=200)


class PasswordResetConfirmAPIView(GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        code = serializer.validated_data['code']
        new_password = serializer.validated_data['new_password']

        reset_obj = PasswordResetCode.objects.filter(email=email, code=code).order_by('-created_at').first()
        if not reset_obj or reset_obj.is_expired():
            return Response({'error': 'Неверный или просроченный код'}, status=400)

        user = CustomUser.objects.filter(email=email).first()
        if not user:
            return Response({'error': 'Пользователь не найден'}, status=404)

        user.set_password(new_password)
        user.save()
        reset_obj.delete()

        return Response({'message': 'Пароль успешно изменён'}, status=200)