from django.contrib import admin
from .models import BloodDonation

class BloodDonationAdmin(admin.ModelAdmin):
    list_display = ('donor', 'blood_type', 'units_donated', 'donation_date', 'hospital', 'confirm')
    search_fields = ('donor__username', 'blood_type', 'hospital__username')
    list_filter = ('blood_type', 'confirm', 'donation_date')
    date_hierarchy = 'donation_date'

admin.site.register(BloodDonation, BloodDonationAdmin)
