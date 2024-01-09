from django.views.generic import CreateView, ListView, DeleteView, UpdateView, DetailView
from django.contrib.auth.views import redirect_to_login
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.views import View
from ..forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from ..filters import CenterFilter, EventFilter
from django.shortcuts import render
from django.contrib.auth.mixins import PermissionRequiredMixin
from ..serializers import *
from django.http import Http404
from django.urls import reverse

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


class HomePage(ListView):
    template_name = 'homepage.html'
    context_object_name = 'urgents'

    def get_queryset(self):
        return Center.objects.filter(tags__name__in=["urgent care"]).order_by('name')
    
    def get_context_data(self, **kwargs):
        context = super(HomePage, self).get_context_data(**kwargs)

        context['centers'] = Center.objects.all().order_by('name')[:3]
        context['upcoming_clinics'] = ClinicEvent.objects.filter(is_active = False).order_by('start_date')[:5]
        context['articles'] = NewsArticle.objects.filter(is_global = True).order_by('date')[:5]
        context['pinned_articles'] = NewsArticle.objects.filter(tags__name__in=["pinned"]).order_by('date').reverse()[:6]

        if self.request.user.is_authenticated:
            context['has_address'] = Address.objects.filter(user = self.request.user).exists()

        return context


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
    model = NewsArticle
    context_object_name = "article_data"
    template_name="article.html"


    slug_url_kwarg = 'email'
    slug_field = 'email'
    
class ArticleList(ListView):
    queryset = NewsArticle.objects.all().order_by('id')
    template_name = 'news_list.html'
    context_object_name = 'articles'
    paginate_by = 1
    
    def get_template_names(self, *args, **kwargs):
        if self.request.htmx:
            return "includes/article-list.html"
        else:
            return self.template_name
        
    def get_context_data(self, **kwargs):
        context = super(ArticleList, self).get_context_data(**kwargs)
        context['pinned_articles'] = NewsArticle.objects.filter(tags__name__in=["pinned"]).order_by('date').reverse()[:6]
        return context

class CenterArticleList(ListView):
    template_name = 'center_articles.html'
    context_object_name = 'articles'
    paginate_by = 1

    def get_queryset(self):
        center_abbreviation = self.kwargs['center_abbreviation']
        return NewsArticle.objects.filter(center_id__center_abbreviation=center_abbreviation).order_by('date').reverse()
    
    def get_template_names(self, *args, **kwargs):
        if self.request.htmx:
            return "includes/center-article-list.html"
        else:
            return self.template_name
        
    def get_context_data(self, **kwargs):
        context = super(CenterArticleList, self).get_context_data(**kwargs)

        center_abbreviation = self.kwargs['center_abbreviation']

        context['center'] = Center.objects.get(center_abbreviation =self.kwargs['center_abbreviation'] )
        context['pinned_articles'] = NewsArticle.objects.filter(tags__name__in=["pinned"], center_id__center_abbreviation=center_abbreviation).order_by('date').reverse()
        return context

class FacilitiesNearMe (LoginRequiredMixin,ListView):

    template_name = 'my_centers.html'         
    context_object_name = "centers"
    paginate_by = 1

    def get_queryset(self):

        profile_add = Address.objects.get(user=self.request.user)
        queryset = Center.objects.filter(district__name =profile_add.district ).order_by('name')
        return queryset
    
class ActiveClinicsNearMe (LoginRequiredMixin,ListView):

    template_name = 'my_active_clinics.html'         
    context_object_name = "active_clinics"
    paginate_by = 2

    def get_queryset(self):

        profile_add = Address.objects.get(user=self.request.user)
        queryset = ClinicEvent.objects.filter(facility__district__name =profile_add.district, is_active=True ).order_by('start_date').reverse()
        print(queryset)
        return queryset
    

class UpcomingClinicsNearMe (LoginRequiredMixin,ListView):

    template_name = 'my_upcoming_clinics.html'         
    context_object_name = "upcoming_clinics"
    paginate_by = 1

    def get_queryset(self):

        profile_add = Address.objects.get(user=self.request.user)
        queryset = ClinicEvent.objects.filter(facility__district__name =profile_add.district,is_active=False ).order_by('start_date').reverse()
        print(queryset)
        return queryset