# forms.py
from django import forms
from .models import DeviceModel, EnrolledDevice

class EnrolledDeviceForm(forms.ModelForm):
    class Meta:
        model = EnrolledDevice
        fields = ['device_model']

    device_type = forms.ChoiceField(choices=[], required=False, widget=forms.RadioSelect)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['device_type'].choices = [(dt, dt) for dt in DeviceModel.objects.values_list('device_type', flat=True).distinct()]
        self.fields['device_model'].queryset = DeviceModel.objects.none()

        if 'device_type' in self.data:
            try:
                device_type = self.data.get('device_type')
                self.fields['device_model'].queryset = DeviceModel.objects.filter(device_type=device_type).order_by('model_name')
            except (ValueError, TypeError):
                pass 