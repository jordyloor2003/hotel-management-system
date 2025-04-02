from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'is_hotel_owner', 'is_customer']

        
    def clean_email(self):
        """Validate that the email is unique"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean(self):
        """Ensure a user can't be both a hotel owner and a customer"""
        cleaned_data = super().clean()
        is_hotel_owner = cleaned_data.get('is_hotel_owner')
        is_customer = cleaned_data.get('is_customer')

        # Verifica que no puedan ser ambos
        if is_hotel_owner and is_customer:
            raise forms.ValidationError("A user cannot be both a hotel owner and a customer at the same time.")
        
        return cleaned_data