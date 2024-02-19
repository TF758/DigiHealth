import django_filters
from django_filters import DateFilter, CharFilter
from .models import *


class EventFilter(django_filters.FilterSet):

    """ Filter to filter clinic events """
    event_name = CharFilter(
        field_name='event_name',
        lookup_expr='icontains',
        label="Search By Clinic Name"
    )
    start_date = DateFilter(
        field_name='start_date',
        lookup_expr='gte',
        label="Search By Date"
    )
    end_date = DateFilter(
        field_name='start_date',
        lookup_expr='lte',
    )
    clinic_type = CharFilter(
        field_name='clinic_type__type_name',
        lookup_expr='icontains',
    )
    facility = CharFilter(
        field_name='facility__name',
        lookup_expr='icontains',
        label="Search By Facility"
    )
    location = CharFilter(
        field_name='facility__district__name',
        lookup_expr='icontains',
        label="Search by District"
    )

    class Meta:
        model = ClinicEvent
        fields = "__all__"
        exclude = ['start_time', 'end_time']

    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        super(EventFilter, self).__init__(
            data=data, queryset=queryset, request=request, prefix=prefix)
        self.filters['start_date'].field.widget.attrs.update(
            {'class': 'datepicker'})
        self.filters['end_date'].field.widget.attrs.update(
            {'class': 'datepicker'})

class CenterFilter(django_filters.FilterSet):
    name = CharFilter(
        field_name='name',
        lookup_expr='icontains',
        label='Filter By Name'
    )
    district = CharFilter(
        field_name='district',
        lookup_expr='icontains',
        label='Filter By District'
    )
   
    class Meta:
        model = Center
        fields = "__all__"
        exclude = ['center_abbreviation', 'contact', 'center_image', 'tags']
      