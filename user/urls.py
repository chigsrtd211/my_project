from django.contrib import admin
from django.urls import path,include
from .views import GuestRegistrationView,OwnerRegistrationView, UserLoginView, OwnerDashboardView, GuestDashboardView, UserRegistrationChoiceView,GuestProfileUpdationView, OwnerProfileUpdationView, PGAvailStatusUpdationView
from django.contrib.auth.views import LogoutView,PasswordChangeView,PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
# from . import views # for mail

urlpatterns = [
    path('guestregistration/',GuestRegistrationView.as_view(),name='guestregistration'),
    path('guestprofileupdation/',GuestProfileUpdationView.as_view(),name='guestprofileupdation'),
    
    path('ownerregistration/',OwnerRegistrationView.as_view(),name='ownerregistration'),
    path('ownerprofileupdation/',OwnerProfileUpdationView.as_view(),name='ownerprofileupdation'),

    path('guest/changepassword/',PasswordChangeView.as_view(template_name = 'guest_dir/guest_changepassword.html', success_url = '/user/guest/changepassword/done'),name='guestchangepassword'),
    path('guest/changepassword/done',PasswordChangeDoneView.as_view(template_name = 'guest_dir/guest_changepassword_done.html'),name='guestchangepassworddone'),
    path('owner/changepassword/',PasswordChangeView.as_view(template_name = 'owner_dir/owner_changepassword.html', success_url = '/user/owner/changepassword/done'),name='ownerchangepassword'),
    path('owner/changepassword/done',PasswordChangeDoneView.as_view(template_name = 'owner_dir/owner_changepassword_done.html'),name='ownerchangepassworddone'),


    path('userlogin/',UserLoginView.as_view(),name='userlogin'),
    path('userlogout/',LogoutView.as_view(),name='userlogout'),
    path('userregistrationchoice/',UserRegistrationChoiceView.as_view(),name='userregistrationchoice'),
    # path('sendmail/',views.sendMail,name='sendmail'),

    path('owner/dashboard/',OwnerDashboardView.as_view(),name='owner_dashboard'),
    path('guest/dashboard/',GuestDashboardView.as_view(),name='guest_dashboard'),

    path('pg/avail_status/update/<int:pk>',PGAvailStatusUpdationView.as_view(),name='pg_availstatus_update'),

    # Forgot Password
    path('password_reset/',PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',PasswordResetCompleteView.as_view(),name='password_reset_complete'),

    
]
