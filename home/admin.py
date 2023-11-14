from django.contrib import admin
from .models import TemporaryHospitalRegistration,CustomRegistration
from import_export.admin import ImportExportModelAdmin
from import_export import resources

class CustomRegistrationResource(resources.ModelResource):
    class Meta:
        model = CustomRegistration


class TemporaryHospitalRegistrationAdmin(admin.ModelAdmin):
    list_display = ('phone', 'email', 'description')
admin.site.register(TemporaryHospitalRegistration, TemporaryHospitalRegistrationAdmin)
 

class CustomRegistrationAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('user', 'usertype', 'phone', 'address','city','blood_type','image')
    search_fields = ('usertype', 'city','blood_type')
    resource_class = CustomRegistrationResource
admin.site.register(CustomRegistration, CustomRegistrationAdmin)


