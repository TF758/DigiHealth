from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.list import ListView
from django.views import View
from ..forms import *
from django.http import JsonResponse
from django.shortcuts import render
from ..serializers import *
from django.core.paginator import Paginator
import string 


class UrgentCareGlobal(ListView):

    """Display page for all all urgent care medical facilities"""

    template_name = 'centers/urgent_care.html'
    context_object_name = 'centers'

    def get_queryset(self):
        return Center.objects.filter(tags__name__in=["urgent care"]).order_by('name')
    
class PHCCentersGlobal(ListView):

    """Display all primary care medical facilities"""

    template_name = 'centers/phc.html'
    context_object_name = 'centers'

    def get_queryset(self):
        return Center.objects.filter(tags__name__in=["phc"]).order_by('name')

class GetCentersByLetter(View):

    """Find a medical center bassed on starting letter(s)"""

    def get(self, request, *args, **kwargs):
        if 'q' in request.GET:
            search_text = request.GET['q']
            search_objects = Center.objects.filter(name__istartswith=search_text).order_by('name')    
        else:
            search_objects = Center.objects.all().order_by('name')
        page_num = request.GET.get("page",1)
        center_paginator = Paginator(search_objects, 3)
        letters = string.ascii_lowercase
        context = {'centers':center_paginator.page(page_num), 'letters': letters}
        return render(request, "centers/center_list.html", context)

    # post request for ajax calls
    def post(self, request, *args, **kwargs):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        if is_ajax:
            query = request.POST['query']
            centers_filtered = Center.objects.filter(
                name__istartswith=query).order_by('name')
            info = HealthCenterSerializer(centers_filtered, many=True)
            center_data = info.data
            return JsonResponse({'centers': list(center_data)})
        return HttpResponse("POST REQUEST MADE")


class CenterDetails(ListView):

    """Page for all data related to specific medical/wellness center"""

    template_name = 'centers/center_details.html'
    context_object_name = 'center_details'

    def get_queryset(self):
        center_abbreviation = self.kwargs['center_abbreviation']
        return Center.objects.get(center_abbreviation=center_abbreviation)
    
    def get_context_data(self, **kwargs):
        context = super(CenterDetails, self).get_context_data(**kwargs)

        center_abbreviation = self.kwargs['center_abbreviation']

        context['center_articles'] =  NewsArticle.objects.filter(centers__center_abbreviation=center_abbreviation).order_by('date').reverse()[:4]
        context['operating_hours'] = OpeningTimes.objects.filter(center__center_abbreviation=center_abbreviation)
        context['address'] = Center.objects.get(center_abbreviation=center_abbreviation).address
        context['active_clinics'] = ClinicEvent.objects.filter( facility__center_abbreviation =center_abbreviation, is_active=True)[:5]
        context['upcoming_clinics'] = ClinicEvent.objects.filter( facility__center_abbreviation =center_abbreviation, is_active=False).order_by('start_date')[:5]
        return context
    
class DistrictCentersDirectory(View):
       
    def get(self, request):
        # check for query pramater in url link
        if 'q' in request.GET:
            search_text = request.GET['q']
            # filter medical facilities by query parameter
            search_objects = Center.objects.filter(district__abbreviation=search_text).order_by('district')  
        else:
            search_objects = Center.objects.all().order_by('district')
        page_num = request.GET.get("page",1)
        # paginate results
        center_paginator = Paginator(search_objects, 3)
        districts = District.objects.all()
        # return updated list of medical facilitie
        context = {'centers':center_paginator.page(page_num), 'districts':districts }
        return render(request, 'centers/district_centers.html', context)