from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Please enter a valid email address.')

    class Meta:
        model = User
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
        }
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')
        help_texts = {
            'first_name': 'Required',
            'last_name': 'Required'
        }
