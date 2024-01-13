# write serializers here
from rest_framework import serializers
from .models import *


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

class DistrictNameSerializer(serializers.ModelSerializer):

    """Returns only name of district"""

    class Meta:
        model = District
        fields = ['name', 'abbreviation']


class ClinicDataSerializer(serializers.ModelSerializer):

    """Returns data about a medical clinic"""

    facility = serializers.CharField(source='facility.name')

    class Meta:
        model = ClinicEvent
        fields = ['id','event_name', 'start_date','end_date','start_time', 'end_time', 'facility']