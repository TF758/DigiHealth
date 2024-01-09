
from django.urls import path, include
from healthapp.appviews import *

from healthapp.api import *

from .appviews import center_views, profile_views, clinic_views, views


urlpatterns = [
    path('', views.HomePage.as_view(), name="home"),
    path('accounts/', include('allauth.urls')), # new

     path('urgent-care',
         center_views.UrgentCareGlobal.as_view(), name='urgent_care_global'),
     path('primary-care',
         center_views.PHCCentersGlobal.as_view(), name='phc_centers_global'),

    path("centers/", center_views.GetCentersByLetter.as_view(), name="centers"),
    path('centers/district/',
        center_views.DistrictCentersDirectory.as_view(), name='centers_all_districts'),
    path("center/<str:center_abbreviation>/",
         center_views.CenterDetails.as_view(), name="center_details"),
         
     path('clinics/active/',
         clinic_views.ActiveClinics.as_view(), name='active_clinics'),
     path('clinics/active/<str:center>/',
         clinic_views.CenterActiveClinics.as_view(), name='center_active_clinics'),
    path('clinics/upcoming/',
         clinic_views.UpcomingClinics.as_view(), name='upcoming_clinics'),
    path('clinics/upcoming/<str:center>/',
         clinic_views.CenterUpcomingClinics.as_view(), name='center_upcoming_clinics'),

    path('profile/<str:email>/',
         profile_views.GetUserProfile.as_view(), name='get_user_profile'),
     path('profile/<str:email>/new',
         profile_views.CreateUserProfile.as_view(), name='create_user_profile'),
    path('profile/<str:email>/update',
         profile_views.UpdateUserProfile.as_view(), name='update_user_profile'),
    path('profile/<str:email>/address/create',
         views.CreateUserAddress.as_view(), name='create_user_address'),
    path('profile/<str:email>/address/update',
         views.UpdateUserAddress.as_view(), name='update_user_address'),
         
    path('news/',
         views.ArticleList.as_view(), name='news'),
     path('news/<str:center_abbreviation>/',
         views.CenterArticleList.as_view(), name='center_news'),
     path('article/<int:pk>',
         views.ViewArticle.as_view(), name='article_details'),
         
    path('near-me/centers/<str:email>',
         views.FacilitiesNearMe.as_view(), name='centers_near_me'),
    path('near-me/clinics/active/<str:email>',
         views.ActiveClinicsNearMe.as_view(), name='active_clinics_near_me'),
    path('near-me/clinics/upcoming/<str:email>',
         views.UpcomingClinicsNearMe.as_view(), name='upcoming_clinics_near_me'),
]