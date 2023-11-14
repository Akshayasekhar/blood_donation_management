from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('contact/', ContactView.as_view(), name='contact'),

    path('login/', LoginView.as_view(), name='login'),
    path('patient_registration/', PatientRegistrationView.as_view(), name='patient_registration'),
    path('donor_registration/', DonorRegistrationView.as_view(), name='donor_registration'),
    path('donor_home/', DonorHomeView.as_view(), name='donor_home'),
    path('patient_home/', PatientHomeView.as_view(), name='patient_home'),
    path('admin_home/', AdminPageView.as_view(), name='admin_home'),
    path('admin_view/', AdminView.as_view(), name='admin_view'),
    path('patient_details/', PatientDetailsView.as_view(), name='patient_details'),
    path('donor_details/', DonorDetailsView.as_view(), name='donor_details'),
    path('hospital_registration/', HospitalRegistrationView.as_view(), name='hospital_registration'),
    path('hospital_self_registration/', HospitalSelfRegistrationView.as_view(), name='hospital_self_registration'),

    path('hospital_details/', HospitalDetailsView.as_view(), name='hospital_details'),
    path('hospital_view/', HospitalView.as_view(), name='hospital_view'),
    path('hospital_home/', HospitalHomeView.as_view(), name='hospital_home'),
    # path('blood_view/', ApprovedBloodView.as_view(), name='blood_view'),
    path('donor/<int:donor_id>/delete/', DonorDeleteView.as_view(), name='delete_donor'),
    path('patient/<int:patient_id>/delete/', PatientDeleteView.as_view(), name='delete_patient'),
    path('hospital/<int:hospital_id>/delete/', HospitalDeleteView.as_view(), name='delete_hospital'),
    path('temp_hospital_registration/', TemporaryHospitalRegistrationView.as_view(), name='temp_hospital_registration'),
    path('requested_hospital/', RequestedHospitalsView.as_view(), name='requested_hospital'),
    path('approve_hospital/<int:hospital_id>/', ApproveHospitalView.as_view(), name='approve_hospital'),
    path('reject_hospital/<int:hospital_id>/', RejectHospitalView.as_view(), name='reject_hospital'),


]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
