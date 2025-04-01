from django.contrib import admin
from .models import Bus , BusStops ,Route , BusAssignment , DriverProfile , DriverBusDetail
# Register your models here.
admin.site.register(BusStops)
admin.site.register(Bus) 
admin.site.register(Route)
# admin.site.register(BusAssignment)

from django import forms
from django.core.exceptions import ValidationError
from .models import BusAssignment, CustomUser

class BusAssignmentForm(forms.ModelForm):
    class Meta:
        model = BusAssignment
        fields = '__all__'

    def clean_students(self):
        students = self.cleaned_data.get("students")
        for student in students:
            existing_assignment = BusAssignment.objects.exclude(id=self.instance.id).filter(students=student)
            if existing_assignment.exists():
                raise ValidationError(f"Student {student.username} is already assigned to another bus.")
        return students


class BusAssignmentAdmin(admin.ModelAdmin):
    filter_horizontal = ('students' ,'bus_stops')  # Enables the multi-select box

    form = BusAssignmentForm

admin.site.register(BusAssignment,BusAssignmentAdmin )

from django.contrib import admin
from .models import DriverProfile

@admin.register(DriverProfile)
class DriverProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'license_number', 'phone_number')
    list_filter = ('user__role',)  
    search_fields = ('user__username', 'license_number')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user__role='driver')
    

admin.site.register(DriverBusDetail)
