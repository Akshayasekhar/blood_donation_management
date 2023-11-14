from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BloodRequest(models.Model):
    BLOOD_TYPES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    units_needed = models.PositiveIntegerField()
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES)
    additional_info = models.TextField(blank=True, null=True)
    hospital = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blood_requests')
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    is_fulfilled = models.BooleanField(default=False)


class BloodUnit(models.Model):
    BLOOD_TYPES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    hospital = models.ForeignKey(User, on_delete=models.CASCADE)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPES)
    units = models.PositiveIntegerField(default=0)