from django.urls import path
from .views import *

urlpatterns = [
    path('hospital_blood_profile/', HospitalBloodView.as_view(), name='hospital_blood_profile'),
    path('donate_blood_form/<int:hospital_id>', BloodDonationFormView.as_view(), name='donate_blood_form'),
    path('blood_donation_view/', BloodDonationView.as_view(), name='blood_donation_view'),
    path('confirm_donation/<int:donation_id>/', ConfirmDonationView.as_view(), name='confirm_donation'),
    path('blood_donation_history/', BloodDonationHistory.as_view(), name='blood_donation_history'),


]