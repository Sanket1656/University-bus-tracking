from django.urls import path
from . import views

app_name = 'tracker'

urlpatterns = [ 
            path('all_buses/' , views.all_buse_view , name='all_buses'),
            path('buses/<int:bus_id>/', views.bus_detail_view, name='bus_detail'),
            path('get_bus_locations/' , views.get_bus_locations , name='get_bus_locations'),
            path('get_bus_stops/' , views.get_bus_stops , name='get_bus_stops'),

]