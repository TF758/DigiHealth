
from django.urls import path, include, register_converter
from allauth.account.views import login
from django.views.generic import TemplateView
from healthapp.views import *
from django.contrib.auth.views import LoginView
# from .api import *

from . import views


urlpatterns = [
    path('', HomePage.as_view(), name="home"),
    path('accounts/', include('allauth.urls')), # new
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
     path('clinics/urgent/',
         UrgentCareGlobal.as_view(), name='urgent_care_global'),
     path('clinics/phc/',
         PHCCentersGlobal.as_view(), name='phc_centers_global'),
    path('profile/<str:email>/',
         GetUserProfile.as_view(), name='get_user_profile'),
     path('profile/<str:email>/new',
         CreateUserProfile.as_view(), name='create_user_profile'),
    path('profile/<str:email>/update',
         UpdateUserProfile.as_view(), name='update_user_profile'),
    path('profile/<str:email>/address/create',
         CreateUserAddress.as_view(), name='create_user_address'),
    path('profile/<str:email>/address/update',
         UpdateUserAddress.as_view(), name='update_user_address'),
     path('article/<int:pk>',
         ViewArticle.as_view(), name='article_details'),
         

]