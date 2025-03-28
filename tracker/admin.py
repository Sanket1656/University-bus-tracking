from django.contrib import admin
from .models import Bus , BusStops ,Route , BusAssignment , DriverProfile , DriverBusDetail
# Register your models here.
admin.site.register(BusStops)
admin.site.register(Bus) 
admin.site.register(Route)
# admin.site.register(BusAssignment)
class BusAssignmentAdmin(admin.ModelAdmin):
    filter_horizontal = ('students' ,'bus_stops')  # Enables the multi-select box

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
