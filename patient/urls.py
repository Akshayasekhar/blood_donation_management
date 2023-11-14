from django.urls import path
from .views import *

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('blood_request_form/', BloodRequestFormView.as_view(), name='blood_request_form'),
    path('blood_request_view/', BloodRequestView.as_view(), name='blood_request_view'),
    path('blood_view/', BloodApprovalView.as_view(), name='blood_view'),
    path('blood_request_history/', BloodRequestHistory.as_view(), name='blood_request_history'),
    path('get_hospitals/', get_hospitals, name='get_hospitals'),

]