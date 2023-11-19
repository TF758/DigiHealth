# write serializers here
from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


# list the name of every health center
class CenterNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Center
        fields = ['name']


class HealthCenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Center
        fields = ['name', 'center_abbreviation', 'district',
                  'contact']
