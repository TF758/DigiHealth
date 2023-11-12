from django.contrib import admin
from .models import *

# Register your models here.



class UserAdmin(admin.ModelAdmin):
    pass


class UserProfileAdmin(admin.ModelAdmin):
    pass


class AddressAdmin(admin.ModelAdmin):
    pass


class DoctorAdmin(admin.ModelAdmin):
    pass


class RadiologyRequestAdmin(admin.ModelAdmin):
    pass


class ArticleAdmin(admin.ModelAdmin):
    pass


class ClinicEventAdmin(admin.ModelAdmin):
    pass


class ClinicTypeAdmin(admin.ModelAdmin):
    pass

admin.site.register(CustomUser, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Address, AddressAdmin)
# admin.site.register(Doctor, DoctorAdmin)
# admin.site.register(RadiologyRequest, RadiologyRequestAdmin)
# admin.site.register(Article, ArticleAdmin)
# admin.site.register(ClinicEvent, ClinicEventAdmin)
# admin.site.register(ClinicType, ClinicEventAdmin)
