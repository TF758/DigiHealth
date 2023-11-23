
from django.urls import path, include, register_converter
from healthapp.views import *

from . import views


urlpatterns = [
    path("", AdminDashBoard.as_view(), name='admin'),
    path("add-center", CreateNewCenter.as_view(), name='new-center'),
    path("manage-centers", ManageCenters.as_view(), name='manage-centers'),
    path("center/delete/<int:pk>", DeleteCenter.as_view(), name='delete-center'),
    path("center/edit/<int:pk>", UpdateCenter.as_view(), name='update-center'),
    path("add-clinic", CreateNewClinicEvent.as_view(), name='new-clinic'),
    path("manage-clinics", ManageClinics.as_view(), name='manage-clinics'),
    path("clinic/delete/<int:pk>", DeleteClinic.as_view(), name='delete-clinic'),
    path("clinic/edit/<int:pk>", UpdateClinic.as_view(), name='update-clinic'),
]
