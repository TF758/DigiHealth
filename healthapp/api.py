from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponseRedirect, HttpResponseNotFound
from rest_framework import generics
  
from .models import *
from .serializers import *
from .forms import *

class CountryDistricts(generics.ListAPIView):
    queryset = District.objects.all()
    serializer_class = DistrictDataSerializer


class DistrictCenters(generics.ListAPIView):
    serializer_class = CenterDataSerializer

    def get_queryset(self):
        district_Id = self.kwargs['district']
        return Center.objects.filter(district__id = district_Id)


class CentersList(generics.ListAPIView):

    """Returns list of all medicial facilities in Saint Lucia"""

    queryset = Center.objects.all()
    serializer_class = CentersDataSerializer


class CenterDetails(generics.RetrieveAPIView):

    """Returns data about a specific medical facility"""
    queryset = Center.objects.all()
    serializer_class = CenterDataSerializer