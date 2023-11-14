from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BloodDonation(models.Model):
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donations')
    blood_type = models.CharField(max_length=10)
    units_donated = models.PositiveIntegerField()
    donation_date = models.DateTimeField(null=True, blank=True)
    hospital = models.ForeignKey(User, on_delete=models.CASCADE) 
    confirm = models.BooleanField(default=False)
