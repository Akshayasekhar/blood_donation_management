from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from geopy.geocoders import Nominatim,ArcGIS
from donor.models import BloodDonation

from home.models import CustomRegistration
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView,PasswordResetConfirmView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from patient.models import BloodRequest, BloodUnit
from cities_light.models import City
from .forms import CityFilterForm 

# Create your views here.
class DonorProfileView(View):
    template_name = 'donor_profile.html'  
    def get(self, request):
        if request.user.is_authenticated:
            try:
                custom_registration_data = CustomRegistration.objects.filter(user=request.user).first()
                if custom_registration_data and custom_registration_data.usertype == 'donor':
    
                    user = request.user
                    custom_registration_data = CustomRegistration.objects.filter(user=user).first()
                    user_data = User.objects.filter(id=user.id).first()
                    blood_donations = BloodDonation.objects.filter(donor=user, confirm=True)
                    total_donations = blood_donations.count()
                    context = {
                    'custom_registration_data': custom_registration_data,
                    'user_data': user_data,
                    'blood_donations': blood_donations,
                    'total_donations': total_donations,
                    }
                    return render(request, self.template_name, context)
                else:
                    return redirect('index') 
            except CustomRegistration.DoesNotExist:
                 return HttpResponse("CustomRegistration does not exist for this user.")                
        else:
            return redirect('index') 

class PatientProfileView(View):
    template_name = 'patient_profile.html'
    def get(self, request):
        if request.user.is_authenticated:
            try:
                custom_registration_data = CustomRegistration.objects.filter(user=request.user).first()
                if custom_registration_data and custom_registration_data.usertype == 'patient':
    
                    user = request.user
                    custom_registration_data = CustomRegistration.objects.filter(user=user).first()
                    user_data = User.objects.filter(id=user.id).first()
                    blood_requests = BloodRequest.objects.filter(patient=user)
                    total_requests = blood_requests.count()
                    context = {
                    'blood_requests': blood_requests,
                    'total_requests': total_requests,

                    'custom_registration_data': custom_registration_data,
                    'user_data': user_data,
                    }
                    return render(request, self.template_name, context)
                else:
                    return redirect('index') 
            except CustomRegistration.DoesNotExist:
                 return HttpResponse("CustomRegistration does not exist for this user.")                
          
        else:
            return redirect('index') 

class HospitalProfileView(View):
    template_name = 'hospital.html'
    def get(self, request):
        if request.user.is_authenticated:
            try:
                custom_registration_data = CustomRegistration.objects.filter(user=request.user).first()
                if custom_registration_data and custom_registration_data.usertype == 'hospital':
    
                     user = request.user
                     custom_registration_data = CustomRegistration.objects.filter(user=user).first()
                     user_data = User.objects.filter(id=user.id).first()
                      # blood_donations = BloodDonation.objects.filter(donor=user, confirm=True)
                      # total_donations = blood_donations.count()

                      # patient_user = request.user
                      # blood_requests = BloodRequest.objects.filter(patient=user)
                       # total_requests = blood_requests.count()

                     city_id = custom_registration_data.city
                     city_name = City.objects.get(id=city_id).name
                     context = {
                      # 'blood_requests': blood_requests,
                      # 'total_requests': total_requests,

                     'custom_registration_data': custom_registration_data,
                     'user_data': user_data,
                     # 'blood_donations': blood_donations,
                     # 'total_donations': total_donations,
                     'city_name':city_name,

                      }
                     return render(request, self.template_name, context)
                else:
                    return redirect('index') 
            except CustomRegistration.DoesNotExist:
                 return HttpResponse("CustomRegistration does not exist for this user.")                
          
        else:
            return redirect('index')      



    
class BaseDeleteAccountView(View):
    template_name = 'delete_account.html'

    def get(self, request):
        if request.user.is_authenticated:
            custom_registration_data = CustomRegistration.objects.filter(user=request.user).first()
            context={
            'custom_registration_data':custom_registration_data,
            }                
            return render(request, self.template_name,context)
        else:
            return redirect('index')
    def post(self, request):
    
        if 'confirm_delete' in request.POST:
            user = request.user

            user.delete()

            try:
                user_data = CustomRegistration.objects.filter(user=user).first()
                user_data.delete()
            except CustomRegistration.DoesNotExist:
                pass

            return redirect('index')

        return render(request, self.template_name)

class DeleteAccountView(BaseDeleteAccountView):
    template_name = 'delete_account.html'

class DeleteAccountPatientView(BaseDeleteAccountView):
    template_name = 'delete_account_patient.html'




       



class EditDonorProfileView(View):
    template_name = 'edit_donor.html'  

    def get(self, request, donor_id):
        if request.user.is_authenticated:
            try:
                custom_registration_data = CustomRegistration.objects.filter(user=request.user).first()
                if custom_registration_data and custom_registration_data.usertype == 'donor':
    
                    user = User.objects.get(pk=donor_id)
                    custom_registration_data = CustomRegistration.objects.filter(user=user).first()

                    context = {
                    'user_data': user,
                    'custom_registration_data' : custom_registration_data,  
            
                     }
                    return render(request, self.template_name, context)
                else:
                    return redirect('index') 
            except CustomRegistration.DoesNotExist:
                 return HttpResponse("CustomRegistration does not exist for this user.")                
              
        else:
            return redirect('login')
    def post(self, request, donor_id):
        if request.user.is_authenticated:
            user = User.objects.get(pk=donor_id)
            custom_registration_data = get_object_or_404(CustomRegistration, user=user)

            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            new_email = request.POST['email']
            new_username = request.POST['username']
            
            if new_username != user.username:
               if User.objects.filter(username=new_username).exclude(pk=patient_id).exists():
                   error_message = "This Username is already registered."
                   return render(request, self.template_name, {'error_message': error_message})
            if new_email != user.email:
                if User.objects.filter(email=new_email).exclude(pk=patient_id).exists():
                    error_message = "This Email is already registered."
                    return render(request, self.template_name, {'error_message': error_message})
            user.username = new_username
            user.email = new_email
        
            user.save()
            if 'image' in request.FILES:
                custom_registration_data.image = request.FILES['image']
            else:
                custom_registration_data.image = None
            custom_registration_data.phone = request.POST['phone']
            custom_registration_data.city = request.POST['city']
            custom_registration_data.blood_type = request.POST.get('bloodType')

            custom_registration_data.address = request.POST['address']
        
            custom_registration_data.save()
            return redirect('donor_profile')  
        else:
            return redirect('index')      

class EditPatientProfileView(View):
    template_name = 'edit_patient.html'  

    def get(self, request, patient_id):
        if request.user.is_authenticated:
            try:
                custom_registration_data = CustomRegistration.objects.filter(user=request.user).first()
                if custom_registration_data and custom_registration_data.usertype == 'patient':
    
                     user = User.objects.get(pk=patient_id)
                     custom_registration_data = get_object_or_404(CustomRegistration, user=user)

                     context = {
                     'user_data': user,
                     'custom_registration_data' : custom_registration_data,  
            
                      }
                     return render(request, self.template_name, context)
                else:
                    return redirect('index') 
            except CustomRegistration.DoesNotExist:
                 return HttpResponse("CustomRegistration does not exist for this user.")    

        else:
            return redirect('index')
    def post(self, request, patient_id):
        user = User.objects.get(pk=patient_id)
        custom_registration_data = get_object_or_404(CustomRegistration, user=user)

        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        new_email = request.POST['email']
        new_username = request.POST['username']
        if new_username != user.username:
            if User.objects.filter(username=new_username).exclude(pk=patient_id).exists():
                error_message = "This Username is already registered."
                return render(request, self.template_name, {'error_message': error_message})
        if new_email != user.email:
            if User.objects.filter(email=new_email).exclude(pk=patient_id).exists():
                error_message = "This Email is already registered."
                return render(request, self.template_name, {'error_message': error_message})
        user.username = new_username
        user.email = new_email

        user.save()
        if 'image' in request.FILES:
                custom_registration_data.image = request.FILES['image']
        else:
                custom_registration_data.image = None
        custom_registration_data.phone = request.POST['phone']
        custom_registration_data.city = request.POST['city']

        custom_registration_data.blood_type = request.POST.get('bloodType')
        custom_registration_data.address = request.POST['address']


        custom_registration_data.save()
        return redirect('patient_profile')            

class EditHospital(EditPatientProfileView):
    template_name = 'edit_hospital.html'  

    def get(self, request, hospital_id):
        if request.user.is_authenticated:
            try:
                custom_registration_data = CustomRegistration.objects.filter(user=request.user).first()
                if custom_registration_data and custom_registration_data.usertype == 'hospital':

                    user = User.objects.filter(pk=hospital_id).first()
                    if user:
                        custom_registration_data = CustomRegistration.objects.filter(user=user).first()
                        city_id = custom_registration_data.city
                        city_name = City.objects.get(id=city_id).name
                        city_filter_form = CityFilterForm()

                        context = {
                        'user_data': user,
                        'custom_registration_data' : custom_registration_data,  
                        'city_name':city_name,
                        'city_filter_form':city_filter_form
                         }
                        return render(request, self.template_name, context)
                else:
                    return redirect('index') 
            except CustomRegistration.DoesNotExist:
                 return HttpResponse("CustomRegistration does not exist for this user.")    
    

        else:
            return redirect('index')  
              
    def post(self, request, hospital_id):
        user = User.objects.get(pk=hospital_id)
        custom_registration_data = CustomRegistration.objects.filter(user=user).first()

        user.first_name = request.POST['first_name']
        new_email = request.POST['email']
        new_username = request.POST['username']
        if new_username != user.username:
            if User.objects.filter(username=new_username).exclude(pk=patient_id).exists():
                error_message = "This Username is already registered."
                return render(request, self.template_name, {'error_message': error_message})
        if new_email != user.email:
            if User.objects.filter(email=new_email).exclude(pk=patient_id).exists():
                error_message = "This Email is already registered."
                return render(request, self.template_name, {'error_message': error_message})
        user.username = new_username
        user.email = new_email
        user.save()
        if 'image' in request.FILES:
                custom_registration_data.image = request.FILES['image']
        else:
                custom_registration_data.image = None
        custom_registration_data.phone = request.POST['phone']
        custom_registration_data.city = request.POST['city']
        custom_registration_data.address = request.POST['address']
        custom_registration_data.save()
        return redirect('hospital')            

from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse_lazy

class CustomPasswordResetView(PasswordResetView):
    template_name = 'custom_password_reset.html' 

    email_template_name = 'custom_password_reset_email.html'  
    subject_template_name = 'custom_password_reset_subject.txt' 
    success_url = reverse_lazy('custom_password_reset')  

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            messages.success(self.request, "Password reset sent. We’ve emailed you instructions for setting your password. You should receive them shortly.")
        else:
            messages.error(self.request, "This email address is not registered.")
        return super().form_valid(form)
    
       
class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'custom_password_reset_confirm.html' 
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['validlink'] = self.validlink
    #     return context       

from django.views.generic import TemplateView

class CustomPasswordResetCompleteView(TemplateView):
    template_name = 'custom_password_reset_complete.html'


class HospitalPasswordChangeView(PasswordChangeView):
    template_name = 'hospital_password_change.html'
    success_url = reverse_lazy('hospital')

    def form_valid(self, form):
        messages.success(self.request, "Your password has been successfully changed.")
        return super().form_valid(form)

class DonorPasswordChangeView(PasswordChangeView):
    template_name = 'donor_password_change.html'
    success_url = reverse_lazy('donor_profile')

    def form_valid(self, form):
        messages.success(self.request, "Your password has been successfully changed.")
        return super().form_valid(form)

class PatientPasswordChangeView(PasswordChangeView):
    template_name = 'password_change.html'
    success_url = reverse_lazy('patient_profile')

    def form_valid(self, form):
        messages.success(self.request, "Your password has been successfully changed.")
        return super().form_valid(form)