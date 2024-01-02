
from django.urls import path
from healthapp.views import *
from healthapp.api import *


urlpatterns = [

     
     # API CALLS - FOR CENTER DATA
     path('districts', CountryDistricts.as_view(), name='api_all_districts'),
     path('centers', CentersList.as_view(), name='api_all_centers'),
     path('centers/urgent', ListUrgentCareCenters.as_view(), name='api_centers_urgent'),
     path('centers/phc', ListPrimaryCareCenters.as_view(), name='api_centers_phc'),
     path('centers/district/<str:district>', DistrictCenters.as_view(), name='api_district_centers'),
     path('center/<str:center_abbreviation>', CenterDetails.as_view(), name='api_center_details'),
     path('center/<str:center_abbreviation>/clinics/active', CenterActiveClinics.as_view(), name='api_center_active_clinics'),
     path('center/<str:center_abbreviation>/clinics/upcoming', CenterUpcomingClinics.as_view(), name='api_center_upcoming_clinics'),
     
     
     # API CALLS FOR CLINICS

     path('clinics', ClinicList.as_view(), name='api_all_clinics'),  
     path('clinics/active', ActiveClinics.as_view(), name='api_active_clinics'),  
     path('clinics/upcoming', UpcomingClinics.as_view(), name='api_upcoming_clinics'),  
     path('clinic/<int:pk>', ClinicDetails.as_view(), name='api_clinic_details'),
     path('clinics/district/<str:district>', DistrictClinics.as_view(), name='api_district_clinics'),
      
]