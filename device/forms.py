from django import forms
from .models import DeviceModel, EnrolledDevice


class EnrolledDeviceForm(forms.ModelForm):

    device_model = forms.ModelChoiceField(
        empty_label='Select Device Model',
        queryset=DeviceModel.objects.all(),
        widget=forms.Select(attrs={'class': 'form-label mt-4'}),
    )

    class Meta:
        model = EnrolledDevice
        fields = ['device_model']


class DeviceTypeForm(forms.Form):

    device_type = forms.ModelChoiceField(
        empty_label='Select Device Type',
        queryset=DeviceModel.objects.all().values_list('device_type', flat=True),
        widget=forms.Select(attrs={'class': 'form-label mt-4'}),
    )

    class Meta:
        fields = ['device_type']
