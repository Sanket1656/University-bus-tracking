from django.urls import path
from . import views

app_name = 'student'

urlpatterns = [ 
    path('', views.student_home, name='home'),
    path('student_profile/', views.student_profile, name='student_profile'),
    path('student_profile_edit/', views.edit_student_profile_view, name='edit_student_profile'),
    path('student_bus_details_edit/', views.edit_student_bus_detail_view, name='edit_student_bus_detail'),
    path('bus_details_view/', views.bus_detail_view, name='bus_detail_view'), 
    path('driver_profile/', views.driver_profile, name='driver_profile'),
    path('driver_profile_edit/', views.edit_driver_profile_view, name='edit_driver_profile'),
    path('bus_details_edit/', views.edit_driver_bus_detail_view, name='edit_driver_bus_detail'),
    path("start_bus/", views.start_bus_tracking, name="start_bus"),
    path("stop_bus/", views.stop_bus_tracking, name="stop_bus"),
]