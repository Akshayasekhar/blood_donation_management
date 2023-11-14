from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from home.models import CustomRegistration
from django.contrib.auth.models import User
from django.conf import settings
from django.core.mail import send_mail

from patient.models import BloodRequest, BloodUnit
from cities_light.models import City
import json


# Create your views here.
class BloodRequestFormView(View):
    template_name = 'blood_request_form.html'

    def get(self, request):
        if request.user.is_authenticated:
            try:
                custom_registration_data = CustomRegistration.objects.filter(user=request.user).first()
                if custom_registration_data and custom_registration_data.usertype == 'patient':
    
                    user_profile = CustomRegistration.objects.filter(user=request.user).first()
                    blood_type = user_profile.blood_type 
                    # hospitals = CustomRegistration.objects.filter(usertype='hospital')
                   
                    cities_data = CustomRegistration.objects.filter(usertype='hospital').values('city').distinct()
                    cities = []
                    for city_data in cities_data:
                         city_id = city_data['city']
                         city = City.objects.filter(id=city_id).values('name').first()
                         cities.append({'id': city_id, 'name': city['name']}) 

                    # selected_city= request.POST.get('city')
                    # hospitals = CustomRegistration.objects.filter(usertype='hospital', city=selected_city)
                   
                    context = {
                #    'hospitals': hospitals,
                   'user': request.user,
                   'blood_type': blood_type,
                   'custom_registration_data':user_profile,
                   'cities':cities,
                    }
                    return render(request, self.template_name, context)
                else:
                    return redirect('index') 
            except CustomRegistration.DoesNotExist:
                return HttpResponse("CustomRegistration does not exist for this user.")           
        else:
            return redirect('login')
    def post(self, request):
        if request.user.is_authenticated:
            patient_user = request.user
            hospital_id = request.POST.get('hospital_id')
            hospital_user = User.objects.get(pk=hospital_id)
            blood_type = request.POST['blood_type']
            units_needed = request.POST['units_needed']
            additional_info = request.POST['additional_info']

            blood_request = BloodRequest(
             patient=patient_user,
             hospital=hospital_user,
             blood_type=blood_type,
             units_needed=units_needed,
             additional_info=additional_info
            )
            blood_request.save()
            send_blood_request_email(hospital_user, patient_user, blood_request)
            return redirect('patient_profile')
        else:
            return redirect('login')
        
from django.http import JsonResponse

def get_hospitals(request):
    city_id = request.GET.get('city_id')
    hospitals = CustomRegistration.objects.filter(usertype='hospital', city=city_id)
    hospitals_data = [{'id': hospital.user.id, 'first_name': hospital.user.first_name} for hospital in hospitals]
    print(hospitals_data)
    return JsonResponse(hospitals_data, safe=False)

class BloodRequestView(View):
    template_name = 'blood_request_view.html'

    def get(self, request):
        if request.user.is_authenticated:
            try:
                custom_registration_data = CustomRegistration.objects.filter(user=request.user).first()
                if custom_registration_data and custom_registration_data.usertype == 'hospital':
    
                    hospital_user = request.user
                    blood_requests = BloodRequest.objects.filter(hospital=hospital_user)

                    user_data = request.user

                    context = {
                    'blood_requests': blood_requests,
                    'user_data': user_data,
                    'custom_registration_data':custom_registration_data,
                    }
                    return render(request, self.template_name, context)
                else:
                    return redirect('index') 
            except CustomRegistration.DoesNotExist:
                return HttpResponse("CustomRegistration does not exist for this user.")          
        else:
            return redirect('login')
class BloodApprovalView(View):
    template_name= 'blood_view.html'
    def get(self, request):
        if request.user.is_authenticated:
            try:
                custom_registration_data = CustomRegistration.objects.filter(user=request.user).first()
                if custom_registration_data and custom_registration_data.usertype == 'hospital':
    
                    hospital_user = request.user
                    blood_units = BloodUnit.objects.filter(hospital=hospital_user)

                    user_data = request.user

                    context = {
                    'blood_units': blood_units,
                    'user_data': user_data,
                    'custom_registration_data':custom_registration_data,
                    }
                    return render(request, self.template_name, context)
                else:
                    return redirect('index') 
            except CustomRegistration.DoesNotExist:
                return HttpResponse("CustomRegistration does not exist for this user.")       
        else:
            return redirect('login')
    def post(self, request):
        if request.user.is_authenticated:
            if 'request_id' in request.POST:
                request_id = request.POST['request_id']
                blood_request = BloodRequest.objects.filter(pk=request_id).first()

                try:
                    approved_unit = BloodUnit.objects.filter(blood_type=blood_request.blood_type).filter(hospital=request.user).first()
                    if approved_unit:
                        approved_unit.units += blood_request.units_needed
                        approved_unit.save()
                    else:
    
                        BloodUnit.objects.create(
                        blood_type=blood_request.blood_type,
                        hospital=request.user,
                        units=blood_request.units_needed,
                        )
                except:
                    pass
                    
                blood_request.is_fulfilled = True
                blood_request.save()

            return redirect('blood_request_view')
        else:
            return redirect('login')    

class BloodRequestHistory(View):
    template_name = 'blood_request_history.html'

    def get(self, request):
        if request.user.is_authenticated:
            try:
                custom_registration_data = CustomRegistration.objects.filter(user=request.user).first()
                if custom_registration_data and custom_registration_data.usertype == 'patient':
    
                    patient_user = request.user
                    blood_requests = BloodRequest.objects.filter(patient=patient_user)
                    total_requests = blood_requests.count()
                    context = {
                    'blood_requests': blood_requests,
                    'total_requests': total_requests,
                    }
                    return render(request, self.template_name, context)   
                else:
                    return redirect('index') 
            except CustomRegistration.DoesNotExist:
                return HttpResponse("CustomRegistration does not exist for this user.")                          
        else:
            return redirect('login')

def send_blood_request_email(hospital_user, patient_user, blood_request):
    subject = 'Blood request from a patient'
    message = f'Hello {hospital_user.first_name},\n\n'
    message += f'{patient_user.first_name} {patient_user.last_name} has requested blood of type {blood_request.blood_type}.\n'
    message += f'Units Needed: {blood_request.units_needed}\n'
    message += f'Additional Information: {blood_request.additional_info}\n'
    from_email = settings.DEFAULT_FROM_EMAIL 
    recipient_list = [hospital_user.email] 
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)