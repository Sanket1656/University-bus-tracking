from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.apps import apps


class CustomUser(AbstractUser):
    role = models.CharField(max_length=20, choices=[
        ('student', 'Student'),
        ('driver', 'Driver'),
    ])
    full_name= models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.full_name

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'student':
            StudentProfile = apps.get_model('student', 'StudentProfile')
            StudentProfile.objects.get_or_create(user=instance)
        elif instance.role == 'driver':
            DriverProfile = apps.get_model('tracker', 'DriverProfile')
            DriverProfile.objects.get_or_create(user=instance)