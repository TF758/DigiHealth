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

class CentersDataSerializer(serializers.ModelSerializer):

    """Used to return data about a group of facilities"""

    google_location = serializers.CharField(source='address')
    district = serializers.CharField(source ='district.name')

    class Meta:
        model = Center
        fields = ['id','name', 'center_abbreviation', 'district',
                  'contact', 'google_location']


class CenterDataSerializer(serializers.ModelSerializer):

    """Used to return data about a specific Medical Facility"""

    google_location = serializers.CharField(source='address')
    district = serializers.CharField(source ='district.name')

    class Meta:
        model = Center
        fields = ['id','name', 'center_abbreviation', 'district',
                  'contact', 'google_location','center_description']


class DistrictDataSerializer(serializers.ModelSerializer):

    """Returns all the districts of Saint Lucia"""

    class Meta:
        model = District
        fields = ['id','name', 'abbreviation']