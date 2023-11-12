from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import *
from django import forms
from collections import OrderedDict
from betterforms import multiform

class AddressForm(forms.ModelForm):
   
    address2 = forms.CharField(max_length=255, required=False)

    class Meta:
        model = Address
        fields = '__all__'
        exclude = ('user',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['gender']
        


class UserCreateForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name','last_name','email', 'password1', 'password2')


class UserProfileMultiForm(multiform.MultiModelForm):
    form_classes = OrderedDict((
        ('user', UserCreateForm),
        ('profile', UserProfileForm),
        ('address', AddressForm),
    ))

    def save(self, commit=True):
        objects = super(UserProfileMultiForm, self).save(commit=False)

        if commit:
            user = objects['user']
            user.save()
            address = objects['address']
            address.user = user
            address.save()
            profile = objects['profile']
            profile.user = user
            profile.address = address
            profile.save()

        return objects

class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email')
