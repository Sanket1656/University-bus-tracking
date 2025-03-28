from django.contrib import admin

# Register your models here.
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'username', 'role')  # Show full_name, username, and role
    list_filter = ('role',)  # Add a filter for role
    search_fields = ('full_name', 'username')  # Add search functionality

admin.site.register(CustomUser, CustomUserAdmin)