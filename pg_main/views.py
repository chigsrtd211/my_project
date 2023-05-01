import os

from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import CreateView
from django.views.generic import DeleteView,UpdateView
from django.views.generic import ListView,DetailView
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView

from .models import PG_Comments, PG_Facility_Master, PG_Amenities, PG_PostAds, PG_Images, PG_Facility, User
from .forms import FacilityMasterCreationForm,PGCreationForm,FacilityCreationForm, PGAmenitiesCreationForm, PGImagesCreationForm, PGCommentsCreationForm, ContactOwnerForm


from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from user.decorators import guest_required,owner_required,superuser_required

from django.contrib.auth import login
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse

# Create your views here.
# ==========================================================================
# PG_PostAds
@method_decorator([login_required(login_url='/user/userlogin'),owner_required],name='dispatch')
class PGCreateView(CreateView):
    form_class = PGCreationForm
    # second_form_class = PGAmenitiesCreationForm
    model = PG_PostAds, User #,PG_Amenities
    template_name = 'pg_dir/create_pg.html'
    success_url = '/user/owner/dashboard'    
   
    def form_valid(self,form):       
        email = self.request.user.email        
        message = 'Thank you for registering your PG in our PG Finder portal.'
        mail_response = 1 #sendMail(email,message)        
        if mail_response > 0:            
            form.instance.owner = self.request.user
            form.save()            
            return super().form_valid(form)
            # return HttpResponse('Mail Sent')
        else:
            return HttpResponse('Failed to send mail') # error page
    
# ------------------------------------------------------------------------
@method_decorator([login_required(login_url='/user/userlogin'),owner_required],name='dispatch')
class PGListView(ListView):

    model = PG_PostAds
    template_name = 'pg_dir/list_pg.html'
    context_object_name = 'pg_list'
    
    def get_queryset(self):
        return super().get_queryset().filter(owner_id=self.request.user.id)    
    
# ------------------------------------------------------------------------
@method_decorator([login_required(login_url='/user/userlogin'),owner_required],name='dispatch')
class PGDeleteView(DeleteView):
    model = PG_PostAds

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)  
      
    success_url = '/user/owner/dashboard'

# ------------------------------------------------------------------------
@method_decorator([login_required(login_url='/user/userlogin'),owner_required],name='dispatch')
class PGUpdateView(UpdateView):
    model = PG_PostAds
    form_class = PGCreationForm
    template_name = 'pg_dir/update_pg.html'
    success_url = '/user/owner/dashboard'

# ------------------------------------------------------------------------
@method_decorator(login_required(login_url='/user/userlogin'),name='dispatch')
class PGDetailView(DetailView):
    model = PG_PostAds
    template_name = 'pg_dir/details_pg.html'
    context_object_name = 'pg_details'

    def get(self, request, *args, **kwargs):
        PGImages = PG_Images.objects.filter(pg_id=self.kwargs['pk'])
        return render(request, 'pg_dir/details_pg.html', {
            'pg_details': self.get_object(),
            'PGImages':PGImages
        })

# ----------------------------------------------------------------
@method_decorator([login_required(login_url='/user/userlogin'),owner_required],name='dispatch')
class PGAmenitiesAddView(CreateView):
    model = PG_Amenities
    form_class = PGAmenitiesCreationForm
    template_name = 'pg_dir/add_pg_amenities.html'
    success_url = '/user/owner/dashboard'

    def form_valid(self, form):
        form.instance.pg = PG_PostAds.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

# ----------------------------------------------------------------

@method_decorator([login_required(login_url='/user/userlogin'),owner_required],name='dispatch')
class PGAmenitiesUpdateView(UpdateView):

    model = PG_Amenities
    form_class = PGAmenitiesCreationForm
    template_name = 'pg_dir/update_pg_amenities.html'
    success_url = '/user/owner/dashboard'

# ----------------------------------------------------------------
@method_decorator([login_required(login_url='/user/userlogin'),owner_required],name='dispatch')
class PGAmenitiesDetailView(DetailView):

    model = PG_Amenities
    template_name = 'pg_dir/detail_pg_amenities.html'
    context_object_name = 'pg_amenities_details'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return self.model.objects.get(pg_id=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

# ----------------------------------------------------------------

@method_decorator([login_required(login_url='/user/userlogin'),owner_required],name='dispatch')
class PGImagesAddView(CreateView):
    model = PG_Images
    form_class = PGImagesCreationForm
    template_name = 'pg_dir/add_pg_images.html'
    # success_url = '/user/owner/dashboard' # need to redirect to the same page

    def get_success_url(self):
        return reverse_lazy('add_pg_images', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        form.instance.pg = PG_PostAds.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

# ----------------------------------------------------------------
@method_decorator([login_required(login_url='/user/userlogin')],name='dispatch')
class PGCommentView(CreateView, ListView):
    model = PG_Comments
    form_class = PGCommentsCreationForm
    template_name = 'pg_dir/add_comment.html'
    # success_url = reverse_lazy('pg_comments') # need to redirect to the same page

    # For CreateView
    def get_success_url(self):
        print('get_success_url')
        return reverse_lazy('pg_comments', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        print('form_valid')
        form.instance.pg = PG_PostAds.objects.get(pk=self.kwargs['pk'])
        form.instance.guest_id = self.request.user.id
        return super().form_valid(form)

    # For ListView
    context_object_name = 'PGComment'
    def get_queryset(self):
        return super().get_queryset().filter(pg=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all().values()
        return context

# ----------------------------------------------------------------
@method_decorator([login_required(login_url='/user/userlogin')],name='dispatch')
class PGCommentsDeleteView(DeleteView):
    model = PG_Comments
    # success_url = '/pg_main/pg/comments'

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)  
    
    def get_success_url(self):
        PGID = PG_Comments.objects.filter(id=self.kwargs['pk']).values()
        # print("PG *********** ",PGID)
        # print("PGID *********** ",PGID[0]['pg_id'])
        return reverse_lazy('pg_comments', kwargs={'pk': PGID[0]['pg_id']})
    
   
# ----------------------------------------------------------------

class ContactOwnerView(FormView):

    model = PG_PostAds,User
    template_name = 'guest_dir/contact_owner.html'
    form_class = ContactOwnerForm    
    success_url = '/pg_main/pg/contact_owner/success'       
            
    def form_valid(self, form):            
        print(form.cleaned_data)        
        # guest details
        guest_email = self.request.user.email                 
        guest_name = self.request.user.first_name                 

        # contact owner form message 
        guest_email_subject = form.cleaned_data.get('subject')                         
        guest_email_message = str(form.cleaned_data.get('message'))
        
        # owner email details and PG Details
        owner_id = PG_PostAds.objects.filter(id=self.kwargs['pk']).values('pg_name','owner_id')                      
        ownerObj = User.objects.filter(id=owner_id[0]['owner_id']).values()        
        owner_email = ownerObj[0]['email']
        # print(owner_email)
        
        # mail message merging
        email = owner_email        

        initial_message = "Greeting from PG Finder Admin!!! \nThere is a good news for you. \nCustomer "+ guest_name + " wants to contact you and negotiate with you regarding your PG " + owner_id[0]['pg_name']
        guest_details_message = "\n\nGuest details are as follow: \nName: - " + guest_name + "\nEmail: - " + guest_email + "\nSubject: - " + guest_email_subject + "\nMessage: - " + guest_email_message
        concluding_message = "\n\nKindly reply to their message. \nTherefore contact " + guest_name + " on their email ID: - " + guest_email + "\n\nThank You !!!"        
        message = initial_message + guest_details_message + concluding_message
                
        # send mail mechanism
        print(email)        
        print(message) 
        mail_response = 1 #sendMail(email,message)
        if mail_response > 0:            
            return super().form_valid(form)
            # return HttpResponse('Mail Sent')
        else:
            return HttpResponse('Failed to send mail') # error page
    
# ----------------------------------------------------------------
class ContactOwnerSuccessView(TemplateView):
    template_name = 'guest_dir/contact_owner_success.html'

# ----------------------------------------------------------------
# @method_decorator([login_required(login_url='/user/userlogin'),owner_required],name='dispatch')
# class PGAvailStatusUpdateView(UpdateView):
#     model = PG_PostAds
#     form_class = PGCreationForm
#     template_name = 'owner_dir/owner_dashboard.html'
#     success_url = '/user/owner/dashboard'

    
        












































































# -------------------------------------------------
def sendMail(email,message): #,request):
    subject = 'PGFinder Admin'      
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]    
    mail_response = send_mail(subject,message,email_from,recipient_list) #recipient_list)
    
    return mail_response
    # if mail_response > 0:
    #     return HttpResponse('Mail Sent')
    # else:
    #     return HttpResponse('Failed to send mail')


# ==========================================================================
# pg_facility_master
class FacilityCreateView(CreateView):
    
    form_class = FacilityMasterCreationForm
    model = PG_Facility_Master
    template_name = 'pg_dir/create_facility.html'
    success_url = '/pg_main/facility/list'

    def form_valid(self, form):
        return super().form_valid(form)

# ------------------------------------------------------------------------
class FacilityDeleteView(DeleteView):
    model = PG_Facility_Master

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)  
      
    success_url = '/pg_main/facility/list'

# ------------------------------------------------------------------------
class FacilityUpdateView(UpdateView):
    model = PG_Facility_Master
    form_class = FacilityMasterCreationForm
    template_name = 'pg_dir/update_facility.html'
    success_url = '/pg_main/facility/list'

# ------------------------------------------------------------------------
class FacilityListView(ListView):

    model = PG_Facility_Master
    template_name = 'pg_dir/list_facility.html'
    context_object_name = 'facility_list'
    
    def get_queryset(self):
        return super().get_queryset()  