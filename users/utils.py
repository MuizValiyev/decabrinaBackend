from django.conf import settings
from django.core.mail import send_mail

def send_otp_code(user_email, otp_code):
    if settings.OTP_BACKEND == 'email':
        print(f"OTP code for {user_email}: {otp_code}")  # вывод в терминал
    else:
        send_mail(
            subject='Ваш OTP код',
            message=f'Ваш код для подтверждения: {otp_code}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user_email],
            fail_silently=False,
        )
    