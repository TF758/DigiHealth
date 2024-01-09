from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import CreateView, FormView, ListView, DeleteView, UpdateView, DetailView
from django.contrib.auth.views import redirect_to_login
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.views import View
from ..forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date, timedelta
from ..filters import CenterFilter, EventFilter
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.mixins import PermissionRequiredMixin
from ..serializers import *
from django.http import Http404
from django.utils.dateparse import parse_date
from django.core.paginator import Paginator
from django.urls import reverse
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta, time

from .views import SetUserMixin

class GetUserProfile(LoginRequiredMixin, DetailView):
    model = CustomUser
    context_object_name = "profile_data"
    template_name="profile/profile_details.html"


    slug_url_kwarg = 'email'
    slug_field = 'email'
    
    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        if not self.request.user:
            qs = qs.filter(pk=self.request.user.pk)
        return qs
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        try:
            context["profile_data"] = UserProfile.objects.get(user = self.request.user)
        except (UserProfile.DoesNotExist):
            context["profile_data"] = False
        try:
            context["user_address"] =  Address.objects.get(user = self.request.user)
        except (Address.DoesNotExist):
            context["user_address"] = False
        return context
  
class CreateUserProfile(SetUserMixin, LoginRequiredMixin, CreateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'profile/profile_data.html'

    def get_success_url(self):
        return reverse('get_user_profile', kwargs={'email': self.kwargs['email']})


class UpdateUserProfile( LoginRequiredMixin,UpdateView):
    model = UserProfile
    fields = ['first_name','last_name','gender']
    template_name = 'profile/profile_data.html'

    slug_field = 'email'
    slug_url_kwarg = 'email'
    
    def get_success_url(self):
        return reverse('get_user_profile', kwargs={'email': self.kwargs['email']})
    
    def get_object(self, queryset=None):
        obj = UserProfile.objects.get(user=self.request.user)
        return obj