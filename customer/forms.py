from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
        }
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')
        
