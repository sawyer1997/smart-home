from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import ServiceLocation


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Please enter a valid email address.')

    class Meta:
        model = User
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
        }
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')


class DateInput(forms.DateInput):
    input_type = 'date'


class ServiceLocationForm(forms.ModelForm):
    class Meta:
        model = ServiceLocation
        fields = ['apt_unit', 'street', 'state', 'zipcode', 'apt_name', 'move_in_date', 'area', 'bedroom', 'occupants']
        widgets = {
            'move_in_date': DateInput(),
        }
