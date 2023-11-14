from django.shortcuts import render,redirect,HttpResponse
from django.views import View
from home.models import CustomRegistration
from patient.models import  BloodUnit,BloodRequest
from itertools import groupby
from django.contrib.auth.models import User
from donor.models import BloodDonation
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from twilio.rest import Client
from cities_light.models import City
from twilio.base.exceptions import TwilioRestException

class HospitalBloodView(View):
    template_name= 'hospital_blood_profile.html'
    def get(self, request):
        if request.user.is_authenticated:
            try:
                custom_registration_data = CustomRegistration.objects.filter(user=request.user).first()
                if custom_registration_data and custom_registration_data.usertype == 'donor':
                     donor_user = CustomRegistration.objects.filter(user=request.user).first()
                     donor_blood_type = donor_user.blood_type
                     blood_units = BloodUnit.objects.all().order_by('hospital__first_name', 'blood_type')
                     custom_registration_data = CustomRegistration.objects.filter( user=request.user).first()
                     cities_data = CustomRegistration.objects.filter(usertype='hospital').values('city').distinct()
                     cities = []
                     for city_data in cities_data:
                         city_id = city_data['city']
                         city = City.objects.filter(id=city_id).values('name').first()
                         cities.append({'id': city_id, 'name': city['name']}) 
                     grouped_data = {}
                     for hospital, group in groupby(blood_units, key=lambda unit: unit.hospital):
                         grouped_data[hospital] = list(group)
            
                     eligible = True
                     last_donation = BloodDonation.objects.filter(donor=request.user).last()
                     if last_donation:
                         last_donation_date = last_donation.donation_date
                         if last_donation_date:
                            three_months_ago = timezone.now() - timezone.timedelta(days=90)
                            if last_donation_date < three_months_ago:
                               eligible = True
                            else:
                               eligible = False
                     else:
                        eligible = True   

                     context = {
                       'grouped_data': grouped_data,
                       'eligible':eligible,
                       'custom_registration_data':custom_registration_data,
                       'cities':cities,
                       "donor_blood_type":donor_blood_type,
                       'blood_units':blood_units
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
            selected_city= request.POST.get('city')
            user_ids = CustomRegistration.objects.filter(usertype='hospital', city=selected_city).values_list('user_id',flat=True)

            blood_units = BloodUnit.objects.filter(hospital_id__in=user_ids).order_by('hospital__first_name', 'blood_type')
            donor_user = CustomRegistration.objects.filter(user=request.user).first()
            donor_blood_type = donor_user.blood_type
            cities_data = CustomRegistration.objects.filter(usertype='hospital').values('city').distinct()
            cities = []
            for city_data in cities_data:
                city_id = city_data['city']
                city = City.objects.filter(id=city_id).values('name').first()
                print(city)
                cities.append({'id': city_id, 'name': city['name']}) 
            custom_registration_data = CustomRegistration.objects.filter(user=request.user).first()

            grouped_data = {}
            for hospitals, group in groupby(blood_units, key=lambda unit: unit.hospital):
                grouped_data[hospitals] = list(group)

            eligible = True
            last_donation = BloodDonation.objects.filter(donor=request.user).last()
            if last_donation:
                last_donation_date = last_donation.donation_date
                if last_donation_date:


                    three_months_ago = timezone.now() - timezone.timedelta(days=90)
                    if last_donation_date < three_months_ago:
                        eligible = True
                    else:
                        eligible = False
            else:
                eligible = True 
            context = {
                'blood_units': blood_units,
                'custom_registration_data': custom_registration_data,
                'selected_city': selected_city,  
                'grouped_data':grouped_data,
                'cities':cities,
                'eligible':eligible,
                "donor_blood_type":donor_blood_type,

            }
       
            return render(request, self.template_name, context)
        else:
            return redirect('login')

   
class BloodDonationFormView(View):
    template_name = 'donate_blood_form.html'

    def get(self, request,hospital_id):
        if request.user.is_authenticated:
            try:
                custom_registration_data = CustomRegistration.objects.filter(user=request.user).first()
                if custom_registration_data and custom_registration_data.usertype == 'donor':
             
                   user_profile = CustomRegistration.objects.filter(user=request.user).first() 
                   hospital = User.objects.filter(pk=hospital_id).first()
                   custom_registration_data = CustomRegistration.objects.filter(user=request.user).first()

                   context = {
                   'user': request.user,
                   'blood_type': user_profile.blood_type ,
                   'hospital_name': hospital.first_name,
                   'custom_registration_data':custom_registration_data,
            
                   }
                   return render(request, self.template_name, context)
                else:
                    return redirect('index') 
            except CustomRegistration.DoesNotExist:
                return HttpResponse("CustomRegistration does not exist for this user.")     
        else:
            return redirect('login')


    def post(self, request,hospital_id):
        if request.user.is_authenticated:
            donor_user = request.user
            hospital_user = User.objects.filter(pk=hospital_id).first()
            blood_type = request.POST.get('blood_type')
            units_donated = request.POST.get('units_donated')
        

            blood_donated = BloodDonation(
                donor=donor_user,
                hospital=hospital_user,
                blood_type=blood_type,
                units_donated=units_donated,
           
            )
            blood_donated.save()
            send_blood_donation_email(hospital_user, donor_user, blood_donated)


            return redirect('donor_profile')    
        else:
            return redirect('login')
class BloodDonationView(View):
    template_name = 'blood_donation_view.html'

    def get(self, request):
        if request.user.is_authenticated:
            try:
                custom_registration_data = CustomRegistration.objects.filter(user=request.user).first()
                if custom_registration_data and custom_registration_data.usertype == 'hospital':
                    hospital_user = request.user

                    donations = BloodDonation.objects.filter(hospital=hospital_user)
                    context = {
                    'donations': donations,
                    'user_data':hospital_user,
                    'custom_registration_data':custom_registration_data,
                    }
                    return render(request, self.template_name, context)
                else:
                    return redirect('index') 
            except CustomRegistration.DoesNotExist:
                return HttpResponse("CustomRegistration does not exist for this user.")         
        else:
            return redirect('login')

class ConfirmDonationView(View):
    template_name = 'blood_donation_view.html'
    def send_sms(self, to, message):
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        
        message = client.messages.create(
            body=message,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=to
        )
    def post(self, request,donation_id):
        if request.user.is_authenticated:
            try:
                donation = BloodDonation.objects.filter(pk=donation_id).first()

                if not donation.confirm:
                    donation.confirm = True
                    donation.donation_date = timezone.now()
                    donation.save()
                    custom= CustomRegistration.objects.get(user=donation.donor)
                    custom_message = (
                       "Send from Blood Donation Management Team.\n"
                       "Thank you for your blood donation. "
                       "Now you are a part of  our mission to save lives through blood donation. "
                       "Donate blood, save a life."
                    )
                    recipient_number = custom.phone
                    self.send_sms(recipient_number, custom_message)

                blood_unit = BloodUnit.objects.filter(blood_type=donation.blood_type,hospital=donation.hospital).first()

                blood_unit.units= blood_unit.units - donation.units_donated
                blood_unit.save()
                if blood_unit.units <= 0:
                        blood_unit.delete()

                return redirect('blood_donation_view')
            except TwilioRestException: 
                error_message ="Invalid or unverified phone number. Please verify phone number with Twilio."
                return render(request, self.template_name, {'error_message': error_message})

        else:
             return redirect('login')

class BloodDonationHistory(View):
    template_name = 'blood_donation_history.html'

    def get(self, request):
        if request.user.is_authenticated:
            try:
                custom_registration_data = CustomRegistration.objects.filter(user=request.user).first()
                if custom_registration_data and custom_registration_data.usertype == 'donor':
                     donor_user = request.user
                     blood_donations = BloodDonation.objects.filter(donor=donor_user, confirm=True)
                     total_donations = blood_donations.count()
                     context = {
                     'blood_donations': blood_donations,
                     'total_donations': total_donations,
                     }
                     return render(request, self.template_name, context)   
                else:
                    return redirect('index') 
            except CustomRegistration.DoesNotExist:
                return HttpResponse("CustomRegistration does not exist for this user.")                
        else:
            return redirect('login')
            
def send_blood_donation_email(hospital_user, donor_user, blood_donated):
    subject = 'Blood donation from a Donor'
    message = f'Hello {hospital_user.first_name},\n\n'
    message += f'{donor_user.first_name} {donor_user.last_name} has expressed interest in donating blood of type {blood_donated.blood_type}.\n'
    message += f'Units Donated: {blood_donated.units_donated}\n'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [hospital_user.email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
