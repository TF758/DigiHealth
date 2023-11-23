from django.contrib import admin
from .models import *

# Register your models here.



class UserAdmin(admin.ModelAdmin):
    filter_horizontal=['groups']


class UserProfileAdmin(admin.ModelAdmin):
    pass


class AddressAdmin(admin.ModelAdmin):
    pass


class ClinicEventAdmin(admin.ModelAdmin):
    pass


class ClinicTypeAdmin(admin.ModelAdmin):
    pass


class WellnessCenterAdmin(admin.ModelAdmin):
    pass


class OpeningHoursAdmin(admin.ModelAdmin):
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
admin.site.register(ClinicEvent, ClinicEventAdmin)
admin.site.register(ClinicType, ClinicTypeAdmin)
admin.site.register(Center, WellnessCenterAdmin)
admin.site.register(OpeningHours, OpeningHoursAdmin)
admin.site.register( Article, ArticleAdmin)
