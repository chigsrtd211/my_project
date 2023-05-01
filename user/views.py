from urllib import request
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic.edit import FormView
from pg_main.forms import PGCreationForm
from .models import User
from pg_main.models import *
from .forms import GuestRegistrationForm,OwnerRegistrationForm, OwnerUpdationForm, GuestUpdationForm, PGAvailStatusUpdationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.conf import settings
from django.core.mail import send_mail
from django.views.generic import ListView
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from user.decorators import guest_required,owner_required
# Create your views here.
# ----------------------------------------------------------------
# @login_required
@method_decorator(login_required(login_url='/user/userlogin'),name='dispatch')
class OwnerDashboardView(ListView):   

    model = PG_PostAds,User
    # form_class = PGAvailStatusUpdationForm
        
    def get(self, request, *args, **kwargs):            
        PGObj = PG_PostAds.objects.filter(owner_id=self.request.user.id)             
        PG_AmenitiesObj = PG_Amenities.objects.all().values()
                
        # Searching logic        
        input = request.GET.get('input')
        print(input)
        # PGObj=[]
        if input:
            PGObj = PG_PostAds.objects.filter(pg_name__icontains=input)
            print(PGObj)
            return render(request, self.template_name,{
                'PG':PGObj,'PG_Amenities':PG_AmenitiesObj
            })            
        else:
            # PGObj = PG_PostAds.objects.all() 
            return render(request, self.template_name,{
                'PG':PGObj, 'PG_Amenities':PG_AmenitiesObj
            })               
         
        # return render(request, 'owner_dir/owner_dashboard.html',{
        #     'PG':PGObj, 'PG_Amenities':PG_AmenitiesObj
        # })
            
    template_name = 'owner_dir/owner_dashboard.html'
    

@method_decorator(login_required(login_url='/user/userlogin'),name='dispatch')
class PGAvailStatusUpdationView(UpdateView):

    model = PG_PostAds
    form_class = PGAvailStatusUpdationForm
    template_name = 'owner_dir/owner_dashboard.html'
    success_url = 'user/owner/dashboard'


# ----------------------------------------------------------------
@method_decorator(login_required(login_url='/user/userlogin'),name='dispatch')
class GuestDashboardView(ListView):    
    
    model = PG_PostAds,User

    def get(self, request, *args, **kwargs):         

        # PGObj = PG_PostAds.objects.select_related('owner').all()
        PGObj = PG_PostAds.objects.all()#.values()
        OnwerObj = User.objects.all().filter(is_owner=True)
        
        UserObj = User.objects.filter(id=self.request.user.id).values()

        # sorting logic
        sort_by = self.request.GET.get('sort_by', '') #price
        sort_direction = self.request.GET.get('sort_direction', '')
        
        if sort_direction == 'asc' and sort_by == 'price':
            PGObj =  PGObj.order_by(sort_by)            
        elif sort_direction == 'desc' and sort_by == 'price':
            PGObj = PGObj.order_by(f'-{sort_by}')
        elif sort_direction == 'asc' and sort_by == 'no_of_rooms':
            PGObj =  PGObj.order_by(sort_by)  
        elif sort_direction == 'desc' and sort_by == 'no_of_rooms':
            PGObj =  PGObj.order_by(f'-{sort_by}')
        else:
            PGObj = PG_PostAds.objects.all()

        # Searching logic        
        input = request.GET.get('input' )
        print(input)
        # PGObj=[]
        if input:
            PGObj = PG_PostAds.objects.filter(pg_name__icontains=input)
            print(PGObj)
            return render(request, self.template_name,{
                'PG':PGObj,'user':UserObj, 'owner_details':OnwerObj
            })            
        else:
            # PGObj = PG_PostAds.objects.all() 
            return render(request, self.template_name,{
                'PG':PGObj,'user':UserObj, 'owner_details':OnwerObj
            })               
         

        # return render(request, self.template_name,{
        #         'PG':PGObj,'user':UserObj, 'owner_details':OnwerObj
        # }) 
    template_name = 'guest_dir/guest_dashboard.html'


# --------------------- ----------------------------------------------------
class GuestRegistrationView(CreateView):
    model = User
    form_class = GuestRegistrationForm
    template_name = 'user_dir/guest_registration.html'    
    success_url = '/user/userlogin/'

    def form_valid(self,form):
        email = form.cleaned_data.get('email') # ??
        message = 'Thank you for your registration in PG Finder as new Guest!!!'
        mail_response = sendMail(email,message)        
        if mail_response > 0:
            user = form.save()
            login(self.request,user)
            return super().form_valid(form)
            # return HttpResponse('Mail Sent')
        else:
            return HttpResponse('Failed to send mail') # error page
       

# -------------------------------------------------------------------------
@method_decorator([login_required(login_url='/user/userlogin'),guest_required],name='dispatch')
class GuestProfileUpdationView(UpdateView):
    model = User
    form_class = GuestUpdationForm
    template_name = 'user_dir/guest_profile_updation.html'    
    success_url = '/user/guest/dashboard'

    def get_object(self, queryset=None):
        return self.request.user
     
# -------------------------------------------------------------------------
@method_decorator([login_required(login_url='/user/userlogin'),owner_required],name='dispatch')
class OwnerProfileUpdationView(UpdateView):
    model = User
    form_class = OwnerUpdationForm
    template_name = 'user_dir/owner_profile_updation.html'        
    success_url = '/user/owner/dashboard/'

    def get_object(self, queryset=None):
        return self.request.user

# -------------------------------------------------------------------------
class OwnerRegistrationView(CreateView):
    model = User
    form_class = OwnerRegistrationForm
    template_name = 'user_dir/owner_registration.html'
    success_url = '/user/userlogin/'


    def form_valid(self,form):
        email = form.cleaned_data.get('email') # ?? silently failed validation
        message = 'Thank you for your registration in PG Finder as a PG Owner!!!'
        mail_response = sendMail(email,message)        
        if mail_response > 0:
            user = form.save()
            login(self.request,user)
            return super().form_valid(form)
            # return HttpResponse('Mail Sent')
        else:
            return HttpResponse('Failed to send mail') # error page

# -------------------------------------------------------------------------

class UserRegistrationChoiceView(ListView):
    model = User
    template_name = 'user_dir/user_registration_choice.html'

# -------------------------------------------------------------------------
class UserLoginView(LoginView):
    template_name = 'user_dir/user_login.html'
    #success_url = "/"
    
    def get_redirect_url(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_guest:
                return '/user/guest/dashboard/'
            elif self.request.user.is_owner:
                return '/user/owner/dashboard/' 
            else:
                return '/error/'

# -------------------------------------------------------------------------
# it should be possible to enable the mail on/off by admin
def sendMail(email,message): #,request):
    subject = 'Registration mail'    
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    mail_response = send_mail(subject,message,email_from,recipient_list) #recipient_list)
    
    return mail_response
    # if mail_response > 0:
    #     return HttpResponse('Mail Sent')
    # else:
    #     return HttpResponse('Failed to send mail')
    


# -------------------------------------------------------------------------
def landingPage(request):
    return render(request, 'index.html')

