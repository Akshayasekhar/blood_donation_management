from django.contrib import admin
from .models import BloodRequest,BloodUnit

# Register your models here.
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ('units_needed', 'blood_type', 'additional_info','hospital','patient','request_date','is_fulfilled')
admin.site.register(BloodRequest, BloodRequestAdmin)
 

class BloodUnitAdmin(admin.ModelAdmin):
    list_display = ('hospital', 'blood_type', 'units')
admin.site.register(BloodUnit, BloodUnitAdmin)
  