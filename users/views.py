from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .models import CustomUser
from .serializers import RegisterSerializer, LoginSerializer, EmailCheckSerializer
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