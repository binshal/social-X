from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views



urlpatterns = [

    path('register/',views.register, name='register'),
    path('',views.CustomLoginView.as_view(), name='login'),
    path('logout/',views.logout_view, name='logout'),
    path('profile/',views.profile_view, name='profile'),
    path('profileupdate/',views.profile_update_view, name='updateprofile'),

    # Password Reset URLs
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset.html',
             email_template_name='accounts/password_reset_email.html',
             subject_template_name='accounts/password_reset_subject.txt',
             success_url='password-reset/done/'
         ),
         name='password_reset'),

    path('password-reset/password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'
         ),
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html',
             success_url='password-reset-complete/'
         ),
         name='password_reset_confirm'),

    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'
         ),
         name='password_reset_complete'),

]
