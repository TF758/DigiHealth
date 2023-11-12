
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
    
]
