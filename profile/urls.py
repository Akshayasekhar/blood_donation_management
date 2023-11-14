from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .views import CustomPasswordResetView
from .views import CustomPasswordResetCompleteView


urlpatterns = [
    path('donor_profile/', DonorProfileView.as_view(), name='donor_profile'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
    path('delete_account/', DeleteAccountView.as_view(), name='delete_account'),
    path('patient_profile/', PatientProfileView.as_view(), name='patient_profile'),
    path('delete_account_patient/', DeleteAccountPatientView.as_view(), name='delete_account_patient'),
    path('hospital/', HospitalProfileView.as_view(), name='hospital'),
    path('edit_donor/<int:donor_id>/', EditDonorProfileView.as_view(), name='edit_donor'),
    path('edit_patient/<int:patient_id>/', EditPatientProfileView.as_view(), name='edit_patient'),
    path('edit_hospital/<int:hospital_id>/', EditHospital.as_view(), name='edit_hospital'),
    # path('profile/<int:donor_id>/', ProfileView.as_view(), name='profile'),
    path('custom_password_reset/', CustomPasswordResetView.as_view(), name='custom_password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset/complete/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('hospital/hospital_password_change/', HospitalPasswordChangeView.as_view(), name='hospital_password_change'),
    path('donor/donor_password_change/', DonorPasswordChangeView.as_view(), name='donor_password_change'),
    path('patient/password_change/', PatientPasswordChangeView.as_view(), name='patient_password_change'),

]

