from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import *
from django import forms
from collections import OrderedDict
from betterforms import multiform
from django.forms import ModelForm

class AddressForm(forms.ModelForm):
   
    address2 = forms.CharField(max_length=255, required=False)

    class Meta:
        model = Address
        fields = '__all__'
        exclude = ('user',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name','gender']

class AddCenterForm(ModelForm):

    class Meta:
        model = Center
        fields = '__all__'
        labels = {
            "name": "Wellness center name",
            "center_abbreviation": "Center Abbrevition",
            "facility": "Clinic Location",
            "district": "District",
            "start_time": "Clinic Start Time",
            "contact": "Contact number",
            "center_image": "Image",
        }

class NewClinicalEventForm(ModelForm):

    class Meta:
        model = ClinicEvent
        fields = '__all__'
        labels = {
            "event_name": "Clinic Name",
            "start_date": "Clinic Start Date",
            "end_date": "Clinic End Date",
            "clinic_type": "Clinic Type",
            "facility": "Clinic Location",
            "clinic_status": "Type of Care",
            "start_time": "Clinic Start Time",
            "end_time": "Clinic End Time",
            "is_active": "Is Clinic Active?",
        }

        widgets = {
            'start_time': forms.TextInput(attrs={'class': 'timepicker'},),
            'end_time': forms.TextInput(attrs={'class': 'timepicker'},),
            'start_date': forms.TextInput(attrs={'class': 'datepicker'},),
            'end_date': forms.TextInput(attrs={'class': 'datepicker'},)

        }
