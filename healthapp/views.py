from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import CreateView, FormView, ListView, DeleteView, UpdateView, DetailView
from django.contrib.auth.views import redirect_to_login
from django.views.generic.list import ListView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views import View
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import date, timedelta
# from .forms import *
from .filters import CenterFilter, EventFilter
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.mixins import PermissionRequiredMixin
from .serializers import *
from django.http import Http404
from django import template
from django.utils.dateparse import parse_date
from django.core.paginator import Paginator

class UserAccessMixin(PermissionRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if (not self.request.user.is_authenticated):
            return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())
        
        if not self.has_permission():
            raise Http404 
        return super(UserAccessMixin, self).dispatch(
                request, *args, **kwargs)
   
   

# # Create your views here.

class AdminDashBoard(View):
    def get(self, request):
        context = {}
        return render(request, "auth/dashboard.html", context)
    
class UserLogin(LoginView):
    form_class = LoginForm
    template_name = 'login.html'
    success_url = reverse_lazy("/")

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('/')

# class CreateNewArticle(LoginRequiredMixin, CreateView):
#     template_name = 'new_article.html'
#     form_class = NewArticleForm
#     model = Article
#     success_url = reverse_lazy("home")


# class ActiveClinics(LoginRequiredMixin, ListView):
#     template_name = 'clinics/active_clinics.html'
#     context_object_name = 'active_clinics'
#     model = ClinicEvent

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['gi_clinics'] = ClinicEvent.objects.filter(
#             is_active=True, facility__district='GI')
#         # context['cas_clinics'] = ClinicEvent.objects.filter(
#         #     is_active=True, facility__district='CAS')
#         return context


def index(request):
    if request.method == 'GET':
        context = {}
        return render(request, "homepage.html", context)


def auth_index(request):
    if request.method == 'GET':
        context = {}
        return render(request, "manage.html", context)


class UserSignupView(CreateView):
    template_name ='register.html'
    form_class = UserProfileMultiForm
    success_url = reverse_lazy('home')

# CENTER MANAGEMENT
   
class CreateNewCenter(UserAccessMixin,CreateView):
    permission_denied_message=""
    permission_required = ("healthapp.add_center")
    redirect_field_name = 'next'
    login_url = '/login/'
    
    model = Center
    success_url = reverse_lazy("manage-centers")
    template_name = 'auth/add-center.html'
    form_class = AddCenterForm

class ManageCenters(UserAccessMixin, View):
    permission_denied_message=""
    permission_required = ("healthapp.add_center",)
    redirect_field_name = 'next'
    login_url = '/login/'

    def get(self, request):
        centers = Center.objects.all()
        center_filter = CenterFilter(request.GET, queryset=centers)
        centers = center_filter.qs
        context = {'center_list': centers, 'center_filter': center_filter}
        return render(request, 'auth/manage-centers.html', context)

class DeleteCenter(UserAccessMixin, DeleteView):
    permission_denied_message=""
    permission_required = ("healthapp.delete_center")
    redirect_field_name = 'next'
    login_url = '/login/'

    model = Center
    success_url = reverse_lazy("manage-centers")
    template_name = "auth/manage-centers.html"


class UpdateCenter(UserAccessMixin, UpdateView):
    permission_denied_message=""
    permission_required = ("healthapp.edit_center")
    redirect_field_name = 'next'
    login_url = '/login/'

    model = Center
    fields = "__all__"
    success_url = reverse_lazy("manage-centers")
    template_name = 'auth/add-center.html'

    
class GetCentersByLetter(View):
    def get(self, request, *args, **kwargs):
        if 'q' in request.GET:
            search_text = request.GET['q']
            search_objects = Center.objects.filter(name__istartswith=search_text).order_by('name')    
        else:
            search_objects = Center.objects.all().order_by('name')
        page_num = request.GET.get("page",1)
        center_paginator = Paginator(search_objects, 1)
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


class CenterDetails(View):
    def get(self, request, *args, **kwargs):
        center_abbreviation = self.kwargs['center_abbreviation']
        center_data = Center.objects.get(center_abbreviation=center_abbreviation)
        articles = Article.objects.filter(center_id__center_abbreviation=center_abbreviation)
        operating_hours =  OpeningHours.objects.filter(center__center_abbreviation=center_abbreviation)
        context = {'center_details': center_data,
                   'center_news': articles, 'address':  center_data.address, 'operating_hours':operating_hours}
        return render(request, 'centers/center_details.html', context)
    
class DistrictCentersDirectory(View):
    def get(self, request):
        if 'q' in request.GET:
            search_text = request.GET['q']
            search_objects = Center.objects.filter(district=search_text).order_by('name')    
        else:
            search_objects = Center.objects.all().order_by('district')
        page_num = request.GET.get("page",1)
        center_paginator = Paginator(search_objects, 10)
        context = {'centers':center_paginator.page(page_num)}

        return render(request, 'centers/district_centers.html', context)


# CLINIC MANAGEMENT
class ManageClinics(LoginRequiredMixin, View):
    def get(self, request):
        events = ClinicEvent.objects.all()
        event_filter = EventFilter(request.GET, queryset=events)
        events = event_filter.qs

        context = {'clinic_list': events, 'event_filter': event_filter}
        return render(request, 'auth/manage-clinics.html', context)


class CreateNewClinicEvent(LoginRequiredMixin, CreateView):
    template_name = 'auth/add-clinic.html'
    form_class = NewClinicalEventForm
    model = ClinicEvent
    success_url = reverse_lazy("manage-clinics")


class DeleteClinic(LoginRequiredMixin, DeleteView):
    model = ClinicEvent
    success_url = reverse_lazy("manage-clinics")



class UpdateClinic(LoginRequiredMixin, UpdateView):
    model = ClinicEvent
    fields = [
        "clinic_type",
        "facility",
        "clinic_status",
        "start_time",
        "end_time",
        "is_active",]
    success_url = reverse_lazy("manage-clinics")
    template_name = 'auth/add-clinic.html'


def futureClinics(request, futuredate):
    if request.method == 'GET':
        next_dates = []
        for i in range(1, 5):
            day = date.today() + timedelta(days=1+i)
            next_dates.append(day)
        date_val = parse_date(futuredate)
        if date_val in next_dates:
            gi_clinics = ClinicEvent.objects.filter(start_date=(
                date_val), facility__district='GI', is_active=False)
            cas_clinics = ClinicEvent.objects.filter(start_date=(
                date_val), facility__district='CAS', is_active=False)
            context = {'gi_clinics': gi_clinics, 'cas_clinics': cas_clinics,
                       'date': date_val}
            return render(request, 'clinics/future.html', context)
        else:
            return HttpResponse(' invalid')


class UpcomingClinics(View):
    def get(self, request):
        upcoming_clinics = []
        next_dates = []

        tomorrow = date.today() + timedelta(days=1)
        for i in range(1, 5):
            day = date.today() + timedelta(days=1+i)
            string_date = str(day)
            date_dict = {day: string_date}
            next_dates.append(date_dict)

        gi_clinics = ClinicEvent.objects.filter(start_date=(
            tomorrow), facility__district='GI', is_active=False)
        cas_clinics = ClinicEvent.objects.filter(start_date=(
            tomorrow), facility__district='CAS', is_active=False)

        print(upcoming_clinics)

        context = {'gi_clinics': gi_clinics, 'cas_clinics': cas_clinics,
                   'next_dates': next_dates, 'upcoming_date':tomorrow}
        return render(request, 'clinics/upcoming.html', context)