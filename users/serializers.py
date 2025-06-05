import random
from django.utils.crypto import get_random_string
from rest_framework import serializers
from .models import CustomUser, OTPSession
from .utils import send_otp_code 



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password']

    def create(self, validated_data):
        return CustomUser.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class EmailCheckSerializer(serializers.Serializer):
    email = serializers.EmailField()


class OTPSessionCreateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)

    def create(self, validated_data):
        email = validated_data['email']
        otp_code = get_random_string(length=6, allowed_chars='0123456789')

        session = OTPSession.objects.create(
            email=email,
            otp_code=otp_code,
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
        )
        
        send_otp_code(email, otp_code)

        return session


class OTPVerifySerializer(serializers.Serializer):
    session_id = serializers.UUIDField()
    otp_code = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            session = OTPSession.objects.get(session_id=data['session_id'], is_used=False)
        except OTPSession.DoesNotExist:
            raise serializers.ValidationError("Сессия не найдена или уже использована")

        if session.is_expired():
            raise serializers.ValidationError("Код истёк")

        if session.otp_code != data['otp_code']:
            session.attempts += 1
            session.save()
            raise serializers.ValidationError("Неверный код")

        session.is_used = True
        session.save()
        data['email'] = session.email
        return data


class NewPasswordSerializer(serializers.Serializer):
    session_id = serializers.UUIDField()
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, data):
        try:
            session = OTPSession.objects.get(session_id=data['session_id'], is_used=True)
        except OTPSession.DoesNotExist:
            raise serializers.ValidationError("Сессия не найдена или не подтверждена")

        try:
            user = CustomUser.objects.get(email=session.email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Пользователь с таким email не найден")

        self.user = user
        return data

    def save(self):
        password = self.validated_data['new_password']
        user = self.user
        user.set_password(password)
        user.save()
        return user
