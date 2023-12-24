from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import CreateView, FormView, ListView, DeleteView, UpdateView, DetailView
from django.contrib.auth.views import redirect_to_login
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.views import View
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date, timedelta
from .filters import CenterFilter, EventFilter
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.mixins import PermissionRequiredMixin
from .serializers import *
from django.http import Http404
from django.utils.dateparse import parse_date
from django.core.paginator import Paginator
from django.urls import reverse
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta, time

class ActiveClinics(ListView):    
    template_name = 'clinics/active.html'  
    context_object_name = "active_clinics"
    model = ClinicEvent    
    paginate_by = 10 
    
    def get_queryset(self):
        events = ClinicEvent.objects.filter(is_active=True).order_by('id')
        event_filter = EventFilter(self.request.GET, queryset=events)
        events = event_filter.qs
        return events
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['event_filter'] = EventFilter()
        return context
    

class UpcomingClinics(ListView):
    queryset  = ClinicEvent.objects.filter(is_active=False).order_by('start_date')  
    template_name = 'clinics/upcoming.html'
    context_object_name = 'upcoming_clinics'
    paginate_by = 2
    
    def get_queryset(self):
        events = ClinicEvent.objects.filter(is_active=False).order_by('start_date')  
        event_filter = EventFilter(self.request.GET, queryset=events)
        events = event_filter.qs
        return events
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['event_filter'] = EventFilter()
        return context
    
class CenterActiveClinics(ListView):    
    template_name = 'clinics/center_active_clinics.html'  
    context_object_name = "active_clinics"    
    paginate_by = 1  
    
    
    def get_queryset(self):
        events = ClinicEvent.objects.filter(is_active=True,facility__center_abbreviation =self.kwargs['center']).order_by('start_date')  
        event_filter = EventFilter(self.request.GET, queryset=events)
        events = event_filter.qs
        return events
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['center'] = Center.objects.get(center_abbreviation =self.kwargs['center'] )
        context['event_filter'] = EventFilter()
        return context

class CenterUpcomingClinics(ListView):    
    template_name = 'clinics/center_upcoming_clinics.html'  
    context_object_name = "upcoming_clinics"    
    paginate_by = 1  
    
    def get_queryset(self):
        events = ClinicEvent.objects.filter(is_active=False,facility__center_abbreviation =self.kwargs['center']).order_by('start_date')  
        event_filter = EventFilter(self.request.GET, queryset=events)
        events = event_filter.qs
        return events
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['center'] = Center.objects.get(center_abbreviation =self.kwargs['center'] )
        context['event_filter'] = EventFilter()
        return context