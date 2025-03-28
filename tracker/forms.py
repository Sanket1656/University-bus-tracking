from django import forms
from .models import DriverProfile , DriverBusDetail


class DriverProfileForm(forms.ModelForm):
    class Meta:
        model = DriverProfile
        fields = ['license_number', 'phone_number', 'address', 'profile_picture']   

class DriverBusDetailForm(forms.ModelForm):
    class Meta:
        model = DriverBusDetail
        fields = ['driver', 'route_select', 'phone_number']    