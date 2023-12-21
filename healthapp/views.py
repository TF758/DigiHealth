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



class UserAccessMixin(PermissionRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if (not self.request.user.is_authenticated):
            return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())
        
        if not self.has_permission():
            raise Http404 
        return super(UserAccessMixin, self).dispatch(
                request, *args, **kwargs)

class SetUserMixin(LoginRequiredMixin):
    user_field = 'user'

    def form_valid(self, form):
        setattr(form.instance, self.user_field, self.request.user)
        return super().form_valid(form)
   
# # Create your views here.

class AdminDashBoard(View):
    def get(self, request):
        context = {}
        return render(request, "auth/dashboard.html", context)
    

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

class HomePage(ListView):
    template_name = 'homepage.html'
    context_object_name = 'urgents'

    def get_queryset(self):
        return Center.objects.filter(tags__name__in=["urgent care"]).order_by('name')
    
    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)

        try:
            profile = UserProfile.objects.get(user = self.request.user.id)
            context['nearby_centers'] = Center.objects.filter(district__name = profile.address.district)[:3]
            context['nearby_active_clinics'] = ClinicEvent.objects.filter(facility__district__name = profile.address.district,is_active = True )[:3]
        except(UserProfile.DoesNotExist):
            context['nearby_centers'] = False
        context['centers'] = Center.objects.all().order_by('name')[:3]
        context['upcoming_clinics'] = ClinicEvent.objects.filter(is_active = False).order_by('start_date')[:5]
        context['articles'] = Article.objects.filter(is_global = True).order_by('date')[:5]
        return context

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


def auth_index(request):
    if request.method == 'GET':
        context = {}
        return render(request, "manage.html", context)

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
        today_start = datetime.combine(today, time())
        today_end = datetime.combine(tomorrow, time())
        
        context['center_news'] =  Article.objects.filter(center_id__center_abbreviation=center_abbreviation)
        context['operating_hours'] = OpeningHours.objects.filter(center__center_abbreviation=center_abbreviation)
        context['address'] = Center.objects.get(center_abbreviation=center_abbreviation).address
        context['active_clinics'] = ClinicEvent.objects.filter(start_date=today, facility__center_abbreviation =center_abbreviation, is_active=True)

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

class ActiveClinics(ListView):
    queryset  = ClinicEvent.objects.filter(is_active=True).order_by('start_date')     
    template_name = 'clinics/active.html'  
    context_object_name = "active_clinics"    
    paginate_by = 12  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['districts'] = ClinicEvent.objects.values_list('facility__district__abbreviation','facility__district__name').filter(is_active=True).distinct()
        return context

    
class ActiveClinicsInDistrict(ListView):    
    template_name = 'clinics/active_district.html'  
    context_object_name = "active_clinics"    
    paginate_by = 1  
    
    def get_queryset(self):
        return ClinicEvent.objects.filter(is_active=True, facility__district__abbreviation =self.kwargs['district'])
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        centers_qs = ClinicEvent.objects.filter(is_active=True, facility__district__abbreviation =self.kwargs['district']).distinct()
        context['centers'] = centers_qs
        context['district'] = District.objects.get(abbreviation =self.kwargs['district'])
        return context

class ActiveClinicsByCenter(ListView):    
    template_name = 'clinics/center_active_clinics.html'  
    context_object_name = "active_clinics"    
    paginate_by = 1  
    
    def get_queryset(self):
        return ClinicEvent.objects.filter(is_active=True, facility__center_abbreviation =self.kwargs['center'])
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['center'] = Center.objects.get(center_abbreviation =self.kwargs['center'] )
        return context



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

class UpcomingClinics(ListView):
    queryset  = ClinicEvent.objects.filter(is_active=False).order_by('start_date')  
    template_name = 'clinics/upcoming.html'
    context_object_name = 'upcoming_clinics'
    paginate_by = 10


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
    
class CreateUserAddress(SetUserMixin, LoginRequiredMixin, CreateView):
    model = Address
    form_class = AddressForm
    template_name = 'profile/profile_data.html'

    def get_success_url(self):
        return reverse('get_user_profile', kwargs={'email': self.kwargs['email']})
    

class UpdateUserAddress( LoginRequiredMixin,UpdateView):
    model = Address
    fields = ['address1','address2','district']
    template_name = 'profile/profile_data.html'

    slug_field = 'email'
    slug_url_kwarg = 'email'
    
    def get_success_url(self):
        return reverse('get_user_profile', kwargs={'email': self.kwargs['email']})
    
    def get_object(self, queryset=None):
        obj = Address.objects.get(user=self.request.user)
        return obj

class ViewArticle( DetailView):
    model = Article
    context_object_name = "article_data"
    template_name="article.html"


    slug_url_kwarg = 'email'
    slug_field = 'email'
    
   