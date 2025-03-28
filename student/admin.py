# student/admin.py
from django.contrib import admin
from .models import StudentProfile, StudentBusDetail

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id', 'department')
    list_filter = ('user__role',)  
    search_fields = ('user__username', 'student_id')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(user__role='student')


@admin.register(StudentBusDetail)
class StudentBusDetailAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'pickup_point', 'route_select', 'department')
    list_filter = ('student_name__role',)  # Add a role filter
    search_fields = ('student_name__username', 'department')
