from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class SignUpForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=[('customer', 'Customer'), ('author', 'Author')],  # Exclude "admin"
        required=True
    )


    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
