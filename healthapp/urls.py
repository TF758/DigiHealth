
from django.urls import path, include, register_converter
from django.views.generic import TemplateView
from healthapp.views import *
from django.contrib.auth.views import LoginView
# from .api import *

from . import views


urlpatterns = [
    path('', views.index),
]
