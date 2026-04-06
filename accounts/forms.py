from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email','first_name','last_name', 'password1', 'password2']


class VendorSignUpForm(CustomUserCreationForm):
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'vendor'
        if commit:
            user.save()
        return user


class CustomerSignUpForm(CustomUserCreationForm):
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'customer'
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='email', required=True)
