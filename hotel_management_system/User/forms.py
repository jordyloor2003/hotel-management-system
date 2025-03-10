from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User  # Aquí le decimos que use nuestro modelo personalizado
        fields = ['username', 'email', 'phone_number', 'is_hotel_owner', 'is_customer', 'password1', 'password2']
