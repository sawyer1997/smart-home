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
        fields = ['apt_unit', 'street', 'state', 'zipcode', 'apt_name', 'move_in_date',
                  'area', 'bedroom', 'occupants']
        widgets = {
            'move_in_date': DateInput(),
        }


class ServiceLocationUpdateForm(forms.ModelForm):

    class Meta:
        model = ServiceLocation
        fields = ['apt_unit', 'street', 'apt_name', 'move_in_date',
                  'area', 'bedroom', 'occupants']
        widgets = {
            'move_in_date': DateInput(),
        }


class ProfileEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class EnergyUsageForm(forms.Form):
    start_date = forms.DateField(
        label='Start Date',
        widget=DateInput()
    )
    end_date = forms.DateField(
        label='End Date',
        widget=DateInput()
    )
    cumulative = forms.BooleanField(
        label='Cumulative',
        required=False
    )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date > end_date:
            raise forms.ValidationError('Start date cannot be greater than End date')

        return cleaned_data

    class Meta:
        fields = ['start_date', 'end_date', 'cumulative']
        widgets = {
            'cumulative': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }


CHOICES = [
    ('11213', '11213'),
    ('08619', '08619'),
]


class ZipCodePrice(forms.Form):
    zipcode = forms.ChoiceField(choices=CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    start_date = forms.DateField(
        label='Start Date',
        widget=DateInput()
    )
    end_date = forms.DateField(
        label='End Date',
        widget=DateInput()
    )
    cumulative = forms.BooleanField(
        label='Cumulative',
        required=False
    )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date >= end_date:
            raise forms.ValidationError('Start date cannot be greater than equal to end date')

        return cleaned_data

    class Meta:
        fields = ['start_date', 'end_date', 'cumulative']
        widgets = {
            'cumulative': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }
