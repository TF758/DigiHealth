
from django.urls import path, include, register_converter
from django.views.generic import TemplateView
from healthapp.views import *
from django.contrib.auth.views import LoginView
# from .api import *

from . import views


urlpatterns = [
    path('', views.index, name="home"),
    path('accounts/', include('allauth.urls')), # new
    path('login/', UserLogin.as_view(), name="login"),
    # path('logout/', Logout.as_view(), name="logout"),
    # path("register/", UserSignupView.as_view(), name='register'),
    path("centers/", GetCentersByLetter.as_view(), name="centers"),
    path("centers/<str:center_abbreviation>/",
         CenterDetails.as_view(), name="center_details"),
    path('centers/district/all',
         DistrictCentersDirectory.as_view(), name='centers_all_districts'),
     path('clinics/active/',
         ActiveClinics.as_view(), name='active_clinics'),
     path('clinics/active/<str:district>/',
         ActiveClinicsInDistrict.as_view(), name='district_active_clinics'),
     path('clinic/active/<str:center>/',
         ActiveClinicsByCenter.as_view(), name='center_active_clinics'),
    path('clinics/future/<str:futuredate>/',
         views.futureClinics, name='future_clinics'),
    path('clinics/upcoming/',
         UpcomingClinics.as_view(), name='upcoming_clinics'),

]