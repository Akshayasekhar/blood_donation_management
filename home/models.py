from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class CustomRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    usertype = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    blood_type = models.CharField(max_length=3)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

class TemporaryHospitalRegistration(models.Model):
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    description = models.TextField()
        