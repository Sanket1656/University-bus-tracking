from django.db import models
from control.models import CustomUser 
from django.core.exceptions import ValidationError

# Create your models here.

class BusStops(models.Model):
    name = models.CharField(max_length=50)
    latitude = models.DecimalField(max_digits=10 , decimal_places=6)
    longitude = models.DecimalField(max_digits=10 , decimal_places=6)
    
    def __str__(self):
        return self.name

class Route(models.Model):
    name = models.CharField(max_length=20 , unique=True)
    start_point = models.ForeignKey(BusStops, on_delete=models.CASCADE, related_name='start_routes')
    end_point = models.ForeignKey(BusStops, on_delete=models.CASCADE, related_name='end_routes')
    bus_stops = models.ManyToManyField(BusStops, related_name='routes')

    def __str__(self):
        return f"{self.name} (From: {self.start_point.name} To: {self.end_point.name})"
    
class Bus(models.Model):
    name = models.CharField(max_length=15,unique=True)
    number_plate = models.CharField(max_length=5, unique=True)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='buses')
    start_point = models.ForeignKey(BusStops, on_delete=models.CASCADE, related_name='start_bus')
    end_point = models.ForeignKey(BusStops, on_delete=models.CASCADE, related_name='end_bus')
    latitude = models.DecimalField(max_digits=10,decimal_places=6)  # Current latitude
    longitude = models.DecimalField(max_digits=10,decimal_places=6)  #Current longitude 
    
    
    def __str__(self):
        return f"{self.name} - {self.route.name}"
    

    
class DriverProfile(models.Model):
    user = models.OneToOneField(
        CustomUser , 
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'driver'}
    )
    license_number = models.CharField(max_length=30, unique=True)
    phone_number = models.CharField(max_length=15, blank=True ,unique=True)
    address = models.TextField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='driver_pics/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.license_number}"
    
class DriverBusDetail(models.Model):
    driver = models.OneToOneField(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'driver'})
    route_select = models.OneToOneField(Route ,on_delete=models.CASCADE )
    phone_number = models.CharField(max_length=15, blank=True)

    def __str__(self):
        return f"{self.driver} - {self.route_select}"
    

    
class BusAssignment(models.Model):
    students = models.ManyToManyField(CustomUser, related_name='bus_assignments', limit_choices_to={'role': 'student'})
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='students')
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='students')
    bus_stops = models.ManyToManyField(BusStops, related_name='assigned_stops')
    driver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assigned_buses',null=True, blank=True ,limit_choices_to={'role': 'driver'})


    def __str__(self):
        return f"{self.bus.name} - {self.route.name}"
    
def clean(self):
        # Get all students that are already assigned to another bus
        for student in self.students.all():
            existing_assignments = BusAssignment.objects.exclude(id=self.id).filter(students=student)
            if existing_assignments.exists():
                raise ValidationError(f"Student {student.username} is already assigned to another bus.")
    
def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    