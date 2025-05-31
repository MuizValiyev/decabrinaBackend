from django import forms
from django.contrib.auth import authenticate
from .models import CustomUser

class EmailForm(forms.Form):
    email = forms.EmailField(label='Email')

class LoginForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user 
    
    def clean(self):
        password = self.cleaned_data.get('password')
        if self.user and not self.user.check_password(password):
            raise forms.ValidationError('Incorrect password')
        
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'password']