from account.views import *
from django.urls import path

urlpatterns = [
    # register user 
    path('register/',UserRegistrationView.as_view(),name = 'register'),
    # login user  
    path('login/',LoginView.as_view(),name = 'login'),
    # logout user
    path('logout/',LogoutView.as_view(),name = 'logout'),
    # afte login visit profile 
    path('profile/',UserProfileView.as_view(),name = 'profile'),
    # change password without email
    path('passwordchange/',ChangePasswordView.as_view(),name = 'passwordchange'),
    # sending mail 
    path('sendemail/',EmailPasswordView.as_view(),name = 'sendemail'),
    # change password with email 
    path('change/<uid>/<token>/',ResetView.as_view(),name = 'change'),


]
