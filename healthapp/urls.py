
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
    path("auth/", AdminDashBoard.as_view(), name='new-center'),
    path("auth/add-center", CreateNewCenter.as_view(), name='new-center'),
    path("auth/manage-centers", ManageCenters.as_view(), name='manage-centers'),
    path("auth/center/delete/<int:pk>", DeleteCenter.as_view(), name='delete-center'),
    path("auth/center/edit/<int:pk>", UpdateCenter.as_view(), name='update-center'),
    path("auth/add-clinic", CreateNewClinicEvent.as_view(), name='new-clinic'),
    path("auth/manage-clinics", ManageClinics.as_view(), name='manage-clinics'),
    path("auth/clinic/delete/<int:pk>", DeleteClinic.as_view(), name='delete-clinic'),
    path("auth/clinic/edit/<int:pk>", UpdateClinic.as_view(), name='update-clinic'),
    path('centers/district/all',
         DistrictCentersDirectory.as_view(), name='centers_all_districts'),
     path('centers/district/<str:district>/',
         CentersByDistrict.as_view(), name='district_wellness_center'),

]
