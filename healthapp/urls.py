
from django.urls import path, include, register_converter
from django.views.generic import TemplateView
from healthapp.views import *
from django.contrib.auth.views import LoginView
# from .api import *

from . import views


urlpatterns = [
    path('', views.index, name="home"),
    path('login/', UserLogin.as_view(), name="login"),
    path('logout/', Logout.as_view(), name="logout"),
    path("register/", UserSignupView.as_view(), name='register'),
    path("center/<str:center_abbreviation>/",
         CenterDetails.as_view(), name="center_details"),
    path('centers/district/all',
         DistrictCentersDirectory.as_view(), name='centers_all_districts'),
     path('centers/district/<str:district>/',
         CentersByDistrict.as_view(), name='district_wellness_center'),

]
