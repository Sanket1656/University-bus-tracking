from django import forms
from .models import StudentProfile , StudentBusDetail


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['student_id', 'department', 'phone_number','address', 'profile_picture']


class StudentBusDetailForm(forms.ModelForm):
    class Meta:
        model = StudentBusDetail
        fields = ['student_name', 'department', 'phone_number','route_select', 'pickup_point']



