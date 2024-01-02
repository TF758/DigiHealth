
from django.urls import path, include, register_converter
from allauth.account.views import login
from django.views.generic import TemplateView
from healthapp.views import *
from django.contrib.auth.views import LoginView
# from .api import *

from . import views
from . import center_views
from . import clinic_views
from . import profile_views
from healthapp.api import *


urlpatterns = [

     
     # API CALLS - FOR CENTER DATA
     path('districts', CountryDistricts.as_view(), name='api_all_districts'),
     path('centers', CentersList.as_view(), name='api_all_centers'),
     path('centers/urgent', ListUrgentCareCenters.as_view(), name='api_centers_urgent'),
     path('centers/phc', ListPrimaryCareCenters.as_view(), name='api_centers_phc'),
     path('centers/district/<int:district>', DistrictCenters.as_view(), name='api_district_centers'),
     path('center/<int:pk>', CenterDetails.as_view(), name='api_center_details'),
     path('center/<int:pk>/clinics/active', CenterActiveClinics.as_view(), name='api_center_active_clinics'),
     path('center/<int:pk>/clinics/upcoming', CenterUpcomingClinics.as_view(), name='api_center_upcoming_clinics'),
     
     
     # API CALLS FOR CLINICS

     path('clinics', ClinicList.as_view(), name='api_all_clinics'),  
     path('clinics/active', ActiveClinics.as_view(), name='api_active_clinics'),  
     path('clinics/upcoming', UpcomingClinics.as_view(), name='api_upcoming_clinics'),  
     path('clinic/<int:pk>', ClinicDetails.as_view(), name='api_clinic_details'),
     path('clinics/district/<int:district>', DistrictClinics.as_view(), name='api_district_clinics'),
      
]