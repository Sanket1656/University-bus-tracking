
from django.conf import settings
from django.db import models 
from tracker.models import BusStops , Route

class StudentProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE , limit_choices_to={'role': 'student'})
    student_id = models.CharField(max_length=20)
    department = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.student_id}"
    

class StudentBusDetail(models.Model):
    student_name = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE , limit_choices_to={'role': 'student'})
    pickup_point = models.ForeignKey(BusStops ,  on_delete=models.CASCADE)
    route_select = models.ForeignKey(Route ,on_delete=models.CASCADE )
    phone_number = models.CharField(max_length=15, blank=True)
    department = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.student_name} - {self.department}"
