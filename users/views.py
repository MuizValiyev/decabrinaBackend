from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .models import CustomUser
from .serializers import RegisterSerializer 

class EmailCheckAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error':'Email is required'},status=400)
        
        exists = CustomUser.objects.filter(email=email).exists()
        return Response({'registered': exists})
    
class LoginAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=400)

        user = authenticate(request, email=email, password=password)
        if user is None:
            return Response({'error': 'Invalid credentials'}, status=401)

        # Можно подключить токен здесь, если хочешь
        return Response({'message': 'Login successful', 'user_id': user.id})


class RegisterAPIView(APIView):
    """
    Регистрация нового пользователя.
    """
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered'}, status=201)
        return Response(serializer.errors, status=400)