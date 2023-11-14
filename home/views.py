from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from donor.models import BloodDonation
import re
from patient.models import BloodRequest, BloodUnit
from .models import CustomRegistration, TemporaryHospitalRegistration
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.db.models import Sum
from geopy.geocoders import Nominatim,ArcGIS
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings
from .forms import CityFilterForm 

class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')

class AboutView(View):
    def get(self, request):
        return render(request, 'about.html')
class RegistrationView(View):
    def get(self, request):
        return render(request, 'registration.html')
class ContactView(View):
    def get(self, request):
        return render(request, 'contact.html')

class HospitalHomeView(View):
    def get(self, request):
        if request.user.is_authenticated:
            try:
                custom_registration_data = CustomRegistration.objects.filter(user=request.user).first()
                if custom_registration_data.usertype == 'hospital':
    
                    user_data = request.user
                    custom_registration_data = CustomRegistration.objects.filter(user=user_data).first()

                    blood_request_total = BloodRequest.objects.filter(hospital_id=user_data).all()
                    blood_request = blood_request_total.count()
                    request_approval = blood_request_total.filter(is_fulfilled='True').count()
                    donation_count_total = BloodDonation.objects.filter(hospital_id=user_data).all()
                    donation_count = donation_count_total.filter(confirm='True').count()
                    donation_request = donation_count_total.count()
                    blood_unit = BloodUnit.objects.filter(hospital_id=user_data).aggregate(total_units=Sum('units'))
                    # today = timezone.now().date()
                    # users_logged_in_today = User.objects.filter(last_login__date=today)
                    # users_logged_in_today_count = users_logged_in_today.count()

                    context = {
                    'user_data': user_data,
                    'donation_count': donation_count,
                    'blood_request': blood_request,
                    'request_approval':request_approval,
                    'donation_request': donation_request,
                    'blood_unit': blood_unit,
                    'custom_registration_data':custom_registration_data,
                     # 'users_logged_in_today_count':users_logged_in_today_count,
                     }
                    return render(request, 'hospital_home.html', context)
                else:
                    return redirect('index')  # Redirect to donor profile if not a patient
            except CustomRegistration.DoesNotExist:
                return HttpResponse("CustomRegistration does not exist for this user.")
        else:
            return redirect('login')



class HospitalView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            custom_registration_data = CustomRegistration.objects.filter(user=user).first()

            context = {

            'user': user,
            'custom_registration_data':custom_registration_data,
            }
            return render(request, 'hospital_view.html', context)
        else:
            return redirect('login')


class AdminView(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.is_staff:
              return render(request, 'admin_view.html')
        else:
            return redirect('login')
from django.utils import timezone


class AdminPageView(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.is_staff:
            total_request = BloodRequest.objects.count()
            total_approved = BloodRequest.objects.filter(is_fulfilled='True').count()
            total_donor_request = BloodDonation.objects.count()
            patient_count = CustomRegistration.objects.filter(usertype='patient').count()
            donor_count = CustomRegistration.objects.filter(usertype='donor').count()
            hospital_count = CustomRegistration.objects.filter(usertype='hospital').count()
            donation_count = BloodDonation.objects.filter(confirm='True').count()
            custom_object = CustomRegistration.objects.all()
            a1_count = custom_object.filter(usertype='patient').filter(blood_type='A+').count()
            a2_count = custom_object.filter(usertype='donor').filter(blood_type='A+').count()
            b1_count = custom_object.filter(usertype='patient').filter(blood_type='B+').count()
            b2_count = custom_object.filter(usertype='donor').filter(blood_type='B+').count()
            ab1_count = custom_object.filter(usertype='patient').filter(blood_type='AB+').count()
            ab2_count = custom_object.filter(usertype='donor').filter(blood_type='AB+').count()
            o1_count = custom_object.filter(usertype='patient').filter(blood_type='O+').count()
            o2_count = custom_object.filter(usertype='donor').filter(blood_type='O+').count()
            a1_count1 = custom_object.filter(usertype='patient').filter(blood_type='A-').count()
            a2_count1 = custom_object.filter(usertype='donor').filter(blood_type='A-').count()
            b1_count1 = custom_object.filter(usertype='patient').filter(blood_type='B-').count()
            b2_count1 = custom_object.filter(usertype='donor').filter(blood_type='B-').count()
            ab1_count1 = custom_object.filter(usertype='patient').filter(blood_type='AB-').count()
            ab2_count1 = custom_object.filter(usertype='donor').filter(blood_type='AB-').count()
            o1_count1 = custom_object.filter(usertype='patient').filter(blood_type='O-').count()
            o2_count1 = custom_object.filter(usertype='donor').filter(blood_type='O-').count()
        
            donor_donations = BloodDonation.objects.values('donor').annotate(total_donations=Count('donor')).filter(confirm=True)

            top_donors = donor_donations.order_by('-total_donations')[:4]
            top_donors_data = User.objects.filter(id__in=[donor['donor'] for donor in top_donors])
            top_donors_info = {}
            for donor in top_donors_data:
               total_donations = next(item['total_donations'] for item in top_donors if item['donor'] == donor.id)
               top_donors_info[donor.id] = {'user': donor, 'total_donations': total_donations}

        
            sorted_top_donors_info = sorted(top_donors_info.values(), key=lambda x: x['total_donations'], reverse=True)
            print(sorted_top_donors_info)

            context = {
            'patient_count': patient_count,
            'donor_count': donor_count,
            'hospital_count': hospital_count,
            'donation_count':donation_count,
            'a1_count': a1_count,
            'a2_count': a2_count,
            'b1_count' : b1_count,
            'b2_count' : b2_count,
            'ab1_count' : ab1_count,
            'ab2_count' :ab2_count,
            'o1_count' : o1_count,
            'o2_count' : o2_count, 'a1_count1': a1_count1,
            'a2_count1': a2_count1,
            'b1_count1' : b1_count1,
            'b2_count1' : b2_count1,
            'ab1_count1' : ab1_count1,
            'ab2_count1' :ab2_count1,
            'o1_count1' : o1_count1,
            'o2_count1' : o2_count1,
            'top_donors_data': top_donors_data,
            'top_donors':top_donors,
            'top_donors_info':top_donors_info,
            'sorted_top_donors_info':sorted_top_donors_info,
            'total_request':total_request,
            'total_approved':total_approved,
            'total_donor_request':total_donor_request,
            }
            return render(request, 'admin_home.html', context)
        else:
            return redirect('login')

# ********************************************************************************************************************************

class PatientDetailsView(View):
    template_name = 'patient_details.html'

    def get(self, request):
        if request.user.is_authenticated and request.user.is_staff:
            patients = CustomRegistration.objects.filter(usertype='patient')
            context = {
            'patients': patients,
            }
            return render(request, self.template_name, context)
        else:
            return redirect('login')
class PatientDeleteView(View):
    def get(self, request, patient_id):
        if requset.user.is_authenticated and request.user.is_staff:
            patient = get_object_or_404(CustomRegistration, id=patient_id)
            patient.delete()
            return redirect('patient_details')
        else:
            return redirect('login')
class DonorDetailsView(View):
    template_name = 'donor_details.html'

    def get(self, request):
        if request.user.is_authenticated and request.user.is_staff:
            donors = CustomRegistration.objects.filter(usertype='donor')
            context = {
            'donors': donors,
            }
            return render(request, self.template_name, context)
        else:
            return redirect('login')

class DonorDeleteView(View):
    def get(self, request, donor_id):
        if request.user.is_authenticated and request.user.is_staff:
            donor = get_object_or_404(CustomRegistration, id=donor_id)
            donor.delete()
            return redirect('donor_details')
        else:
            return redirect('login')

class HospitalDetailsView(View):
    template_name = 'hospital_details.html'

    def get(self, request):
        if request.user.is_authenticated and request.user.is_staff:
            hospitals = CustomRegistration.objects.filter(usertype='hospital')
            context = {
            'hospitals': hospitals,
            }
            return render(request, self.template_name, context)
        else:
            return redirect('login')
class HospitalDeleteView(View):
    def get(self, request, hospital_id):
        if request.user.is_authenticated and request.user.is_staff:
           hospital = CustomRegistration.objects.filter(id=hospital_id)
           hospital.delete()
           return redirect('hospital_details')
        else:
            return redirect('login')

from django.urls import reverse

class UserRegistrationView(View):
    template_name = 'patient_registration.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):

        first_name = request.POST['firstName']
        last_name = request.POST['lastName']
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        usertype = request.POST['usertype']
        phone = request.POST['phone']
        address = request.POST['address']
        city = request.POST['city']
        if 'image' in request.FILES:
              image = request.FILES.get('image')
        else:
              image = None
        blood_type = request.POST.get('bloodType')
        error_message = None
        # if not re.match(r'^+91\d{10,12}$', phone):
        #     error_message = "Please enter a valid phone number."
        #     return render(request, self.template_name, {'error_message': error_message})

        if password != confirm_password:
            error_message = "Passwords do not match."
            return render(request, self.template_name, {'error_message': error_message})

        if User.objects.filter(email=email).exists():
            error_message = "This Email is already registered."
            return render(request, self.template_name, {'error_message': error_message})

        if User.objects.filter(username=username).exists():
            error_message = "This Username is already registered."
            return render(request, self.template_name, {'error_message': error_message})

        user = User.objects.create_user(first_name=first_name,
                                        last_name=last_name,
                                        email=email,
                                        username=username,
                                        password=password,

                                        )
        user.save()
        registration = CustomRegistration(
            user=user,
            usertype=usertype,
            phone=phone,
            address=address,
            city=city,
            blood_type=blood_type,
            image=image,
          
        )
        registration.save()
        send_registration_completion_email_to_user(user)

        return redirect('login')

class DonorRegistrationView(UserRegistrationView):
    template_name = 'donor_registration.html'
    def get(self, request):
        if request.user.is_authenticated:
            custom_registration = CustomRegistration.objects.filter(user=request.user).filter(usertype='donor').first()
            
            if custom_registration:
                return redirect('donor_profile')
            else:
                return render(request, self.template_name)
        else:
            return render(request, self.template_name)
class PatientRegistrationView(UserRegistrationView):
    template_name = 'patient_registration.html'
    def get(self, request):
        if request.user.is_authenticated:
            custom_registration = CustomRegistration.objects.filter(user=request.user).filter(usertype='patient').first()

            if custom_registration:
                return redirect('patient_profile')
            else:
                return render(request, self.template_name)
        else:
            return render(request, self.template_name)


class HospitalRegistrationView(View):
    template_name = 'hospital_registration.html'

    def get(self, request):
        if request.user.is_authenticated:
           return render(request, self.template_name)
        else:
            return redirect('login')
    def post(self, request):
        usertype = request.POST['usertype']
        first_name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        city = request.POST.get('city')
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            error_message = "This Username is already registered."
            return render(request, self.template_name, {'error_message': error_message})
        if User.objects.filter(email=email).exists():
            error_message = "This Email is already registered."
            return render(request, self.template_name, {'error_message': error_message})
       
        user = User.objects.create_user(first_name=first_name,
                                        email=email,
                                        username=username,
                                        password=password,
                                        )
        user.save()
        registration = CustomRegistration(
            user=user,
            usertype=usertype,
            phone=phone,
            address=address,
            city=city,
        )
        registration.save()
        return redirect('hospital_details')

class HospitalSelfRegistrationView(View):
    template_name = 'hospital_self_registration.html'

    def get(self, request):
        city_filter_form = CityFilterForm()
        
        return render(request, self.template_name,{'city_filter_form':city_filter_form})

    def post(self, request):
        usertype = request.POST['usertype']
        first_name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        city = request.POST['city']
        username = request.POST['username']
        password = request.POST['password']
        if 'image' in request.FILES:
            image = request.FILES['image']
        else:
              image = None
       
        if User.objects.filter(username=username).exists():
            error_message = "This Username is already registered."
            return render(request, self.template_name, {'error_message': error_message})
        if User.objects.filter(email=email).exists():
            error_message = "This Email is already registered."
            return render(request, self.template_name, {'error_message': error_message})
    
       
        user = User.objects.create_user(first_name=first_name,
                                        email=email,
                                        username=username,
                                        password=password,
                                        )
        user.save()
        registration = CustomRegistration(
            user=user,
            usertype=usertype,
            phone=phone,
            address=address,
            city=city,
            image=image,
           
        )
        registration.save()
        send_registration_completion_email(user)
        return redirect('login')

class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                return redirect('admin_home')
            custom_registration = CustomRegistration.objects.filter(user=request.user).first()
            if custom_registration:
                if custom_registration.usertype == 'patient':
                    return redirect('patient_profile')
                elif custom_registration.usertype == 'donor':
                    return redirect('donor_profile')
                elif custom_registration.usertype == 'hospital':
                    return redirect('hospital_home')
        return render(request, self.template_name)

    def post(self, request):
        username_or_email = request.POST['username_or_email']  
        password = request.POST['password']
        user = None
        if  username_or_email:
            user = User.objects.filter(username=username_or_email).first()
            if user is None:
                user = User.objects.filter(email=username_or_email).first()

        if user is not None and user.check_password(password):

            if user.is_superuser:
                login(request, user)
                return redirect('admin_home')
            custom_registration = CustomRegistration.objects.filter(user=user).first()
            if custom_registration:
                if custom_registration.usertype == 'patient':
                    login(request, user)
                    return redirect('patient_profile')
                elif custom_registration.usertype == 'donor':
                    login(request, user)
                    return redirect('donor_profile')
                elif custom_registration.usertype == 'hospital':
                    login(request, user)
                    return redirect('hospital_home')
        messages.error(request, 'Invalid username or password') 
            

        return render(request, self.template_name)



class UserHomeView(View):
    template_name = 'donor_home.html'

    def get(self, request):
        return render(request, self.template_name)

class PatientHomeView(UserHomeView):
    template_name = 'patient_home.html'

class DonorHomeView(UserHomeView):
    template_name = 'donor_home.html'
    def get(self, request):
        donor_user = request.user
        blood_donations = BloodDonation.objects.filter(donor=donor_user, confirm=True)
        total_donations = blood_donations.count()



        context = {
            'blood_donations': blood_donations,
            'total_donations': total_donations,

        }

        return render(request, self.template_name, context)            
  

class TemporaryHospitalRegistrationView(View):
    def get(self,request):
        return render(request,'index.html')
    def post(self,request):
        phone=request.POST.get('hospital_phone')    
        email=request.POST.get('hospital_email')  
        description=request.POST.get('hospital_description')   
 
        hospital= TemporaryHospitalRegistration(
            phone=phone,
            email=email,
            description=description,
        )   
        hospital.save()
        return redirect('index')

class RequestedHospitalsView(View):
    template_name = 'requested_hospital.html'
    
    def get(self, request):
        if request.user.is_authenticated and request.user.is_staff:
            hospitals = TemporaryHospitalRegistration.objects.all()
            context = {
            'hospitals': hospitals,
            }
            return render(request, self.template_name, context)        
        else:
            return redirect('login')
class ApproveHospitalView(View):
    def get(self, request, hospital_id):
        if request.user.is_authenticated and request.user.is_staff:
            hospital = TemporaryHospitalRegistration.objects.get(id=hospital_id)
            send_email_to_hospital(hospital.email)
            hospital.delete()
            return redirect('requested_hospital')
        else:
            return redirect('login')

class RejectHospitalView(View):
    def get(self, request, hospital_id):
        if request.user.is_authenticated and request.user.is_staff:
            hospital = TemporaryHospitalRegistration.objects.get(id=hospital_id)
            send_rejection_email(hospital.email)
            hospital.delete()
            return redirect('requested_hospital')
        else:
            return redirect('login')
def send_email_to_hospital(email):
    subject = 'Approval for Hospital Registration'
    # registration_link = reverse('hospital_registration')
    message = 'Your hospital registration Blood Donation Management System has been approved. You can now complete your registration by clicking the following link:\n\n http://127.0.0.1:8000/hospital_self_registration/'
    from_email = 'akshayasekharan21@gmail.com' 
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

def send_rejection_email(email):
    # Send a rejection email to the hospital
    subject = 'Hospital Registration Rejection'
    message = 'We regret to inform you that your hospital registration has been rejected.'
    from_email = 'akshayasekharan21@gmail.com'  
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)        

def send_registration_completion_email(hospital):
    subject = 'Your Hospital Registration with Blood Donation Management is Completed'
    message = f'Hello {hospital.first_name},\n\n'
    message += 'Your registration with Blood Donation Management has been completed. You can now log in using the following credentials:\n'
    message += f'Username: {hospital.username}\n'
    message += f'Registered Email: {hospital.email}\n'

    message += 'Thank you for joining Blood Donation Management. We believe in the power of community and the difference every individual can make. Together, we can save lives through efficient blood donation coordination.\n\n'
    message += 'If you have any questions or need assistance, please contact our support team at support@blooddonationmanagement.com.\n\n'
    message += 'Best regards,\nBlood Donation Management Team'

    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [hospital.email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

def send_registration_completion_email_to_user(user):
    subject = 'Your Registration with Blood Donation Management is Completed'
    message = f'Hello {user.first_name} {user.last_name},\n\n'
    message += 'Your registration with Blood Donation Management has been completed. You can now log in using the following credentials:\n'
    message += f'Username: {user.username}\n'
    message += f'Registered Email: {user.email}\n'

    message += 'Thank you for joining Blood Donation Management. We believe in the power of community and the difference every individual can make. Together, we can save lives through efficient blood donation coordination.\n\n'
    message += 'If you have any questions or need assistance, please contact our support team at support@blooddonationmanagement.com.\n\n'
    message += 'Best regards,\nBlood Donation Management Team'

    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)    






