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


class UrgentCareGlobal(ListView):
    template_name = 'centers/urgent_care.html'
    context_object_name = 'centers'

    def get_queryset(self):
        return Center.objects.filter(tags__name__in=["urgent care"]).order_by('name')
    
class PHCCentersGlobal(ListView):
    template_name = 'centers/phc.html'
    context_object_name = 'centers'

    def get_queryset(self):
        return Center.objects.filter(tags__name__in=["phc"]).order_by('name')

class GetCentersByLetter(View):
    def get(self, request, *args, **kwargs):
        if 'q' in request.GET:
            search_text = request.GET['q']
            search_objects = Center.objects.filter(name__istartswith=search_text).order_by('name')    
        else:
            search_objects = Center.objects.all().order_by('name')
        page_num = request.GET.get("page",1)
        center_paginator = Paginator(search_objects, 10)
        context = {'centers':center_paginator.page(page_num)}
        return render(request, "centers/center_list.html", context)

    def post(self, request, *args, **kwargs):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            query = request.POST['query']
            centers_filtered = Center.objects.filter(
                name__icontains=query).order_by('name')
            info = HealthCenterSerializer(centers_filtered, many=True)
            center_data = info.data
            # print(center_data)
            return JsonResponse({'centers': list(center_data)})
        return HttpResponse("TEST")


class CenterDetails(ListView):
    template_name = 'centers/center_details.html'
    context_object_name = 'center_details'

    def get_queryset(self):
        center_abbreviation = self.kwargs['center_abbreviation']
        return Center.objects.get(center_abbreviation=center_abbreviation)
    
    def get_context_data(self, **kwargs):
        context = super(CenterDetails, self).get_context_data(**kwargs)

        center_abbreviation = self.kwargs['center_abbreviation']
        today = datetime.now().date()
        tomorrow = today + timedelta(1)

        
        context['center_articles'] =  Article.objects.filter(center_id__center_abbreviation=center_abbreviation)[:4]
        context['operating_hours'] = OpeningHours.objects.filter(center__center_abbreviation=center_abbreviation)
        context['address'] = Center.objects.get(center_abbreviation=center_abbreviation).address
        context['active_clinics'] = ClinicEvent.objects.filter( facility__center_abbreviation =center_abbreviation, is_active=True)[:5]
        context['upcoming_clinics'] = ClinicEvent.objects.filter( facility__center_abbreviation =center_abbreviation, is_active=False).order_by('start_date')[:5]

        return context
    
class DistrictCentersDirectory(View):
    def get(self, request):
        if 'q' in request.GET:
            search_text = request.GET['q']
            search_objects = Center.objects.filter(district__abbreviation=search_text).order_by('district')    
        else:
            search_objects = Center.objects.all().order_by('district')
        page_num = request.GET.get("page",1)
        center_paginator = Paginator(search_objects, 10)
        context = {'centers':center_paginator.page(page_num)}

        return render(request, 'centers/district_centers.html', context)