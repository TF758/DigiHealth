
from django.urls import path


from .appviews import views


urlpatterns = [
    path("", views.AdminDashBoard.as_view(), name='admin'),
    path("add-center", views.CreateNewCenter.as_view(), name='new-center'),
    path("manage-centers", views.ManageCenters.as_view(), name='manage-centers'),
    path("center/delete/<int:pk>", views.DeleteCenter.as_view(), name='delete-center'),
    path("center/edit/<int:pk>", views.UpdateCenter.as_view(), name='update-center'),
    path("add-clinic", views.CreateNewClinicEvent.as_view(), name='new-clinic'),
    path("manage-clinics", views.ManageClinics.as_view(), name='manage-clinics'),
    path("clinic/delete/<int:pk>", views.DeleteClinic.as_view(), name='delete-clinic'),
    path("clinic/edit/<int:pk>", views.UpdateClinic.as_view(), name='update-clinic'),
]
