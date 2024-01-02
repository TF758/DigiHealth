from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponseRedirect, HttpResponseNotFound
from rest_framework import generics
  
from .models import *
from .serializers import *
from .forms import *


class ListUrgentCareCenters(generics.ListAPIView):

    """Returns list of all urgent care medical facilities in Saint Lucia"""

    queryset = Center.objects.filter(tags__name__in=["urgent care"]).order_by('name')
    serializer_class = CentersDataSerializer

class ListPrimaryCareCenters(generics.ListAPIView):
    
    """Returns list of all primary care medical facilities in Saint Lucia"""

    queryset = Center.objects.filter(tags__name__in=["phc"]).order_by('name')
    serializer_class = CentersDataSerializer


class CountryDistricts(generics.ListAPIView):
    """Returns list of all districts in Saint Lucia"""
    queryset = District.objects.all()
    serializer_class = DistrictDataSerializer


class DistrictCenters(generics.ListAPIView):

    """Returns list of all medical facilities for a district"""
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


class ClinicList(generics.ListAPIView):

    """Returns list of all active and scheduled clincis that are not expired"""

    serializer_class = ClinicDataSerializer

    def get_queryset(self):
        return ClinicEvent.objects.filter(is_expired = False)
    

class ClinicDetails(generics.RetrieveAPIView):

    """Returns data about a single medical clinic that is not expired"""

    queryset = ClinicEvent.objects.all()
    serializer_class = ClinicDataSerializer

class DistrictClinics(APIView):

    """Returns list of all clinics that are currently active/scheduled in a district"""

    def get(self, request, district):

            qs = ClinicEvent.objects.filter(facility__district__id = district)
            district = District.objects.get(id =district)

            district_name = DistrictNameSerializer(district)
            clinic_list = ClinicDataSerializer(qs, many = True)
            data = {'district':district_name.data,'clinics':clinic_list.data}

            return Response(data )

class ActiveClinics(generics.ListAPIView):

    """Returns list of all active clinics"""

    queryset = ClinicEvent.objects.filter(is_active = True, is_expired = False).order_by('start_date')
    serializer_class = ClinicDataSerializer


class UpcomingClinics(generics.ListAPIView):

    """Returns list of scheduled, non-expired  clinics"""

    queryset = ClinicEvent.objects.filter(is_active = False, is_expired = False).order_by('start_date')
    serializer_class = ClinicDataSerializer


class CenterActiveClinics(APIView):

    """returns list of all active clinics for medical center"""

    def get(self, request, pk):

        qs = ClinicEvent.objects.filter(facility__id = pk,is_active = True, is_expired = False)
        clinic_list = ClinicDataSerializer(qs, many = True).data
        return Response(clinic_list)


class CenterUpcomingClinics(APIView):

    """returns list of all scheduled clincis for medical center"""

    def get(self, request, pk):

        qs = ClinicEvent.objects.filter(facility__id = pk,is_active = False, is_expired = False)
        clinic_list = ClinicDataSerializer(qs, many = True).data
        return Response(clinic_list)