import django_filters
from django.contrib.gis.geos import Point
from api.models import AQIPoint, AQIMeasurement, AQIStandard

class PointFilter(django_filters.FilterSet):
    standard = django_filters.CharFilter(method='filter_by_standard', label='Air quality index standard (High, Medium, Low)')
    coordinates = django_filters.CharFilter(method='filter_by_coordinates', label='Coordinates (latitude, longitude)')

    class Meta:
        model = AQIPoint
        fields = [ 'total_number_measurements', 'last_standard', 'last_measurement_date'] 

    def filter_by_standard(self, queryset, name, value):
        return queryset.filter(measurements__standard__description=value).distinct()
    
    def filter_by_coordinates(self, queryset, name, value):
        try:
            value = value.replace('(', '').replace(')', '').replace(' ', '')
            
            lat, lon = map(float, value.split(','))
            point = Point(lon, lat)
   
            return queryset.filter(coordinates=point)
        
        except (ValueError, TypeError):
            return queryset.none() 
        
class MeasurementFilter(django_filters.FilterSet):
    standard = django_filters.CharFilter(method='filter_by_standard', label='Air quality index standard (High, Medium, Low)')
    coordinates = django_filters.CharFilter(method='filter_by_coordinates', label='Coordinates (latitude, longitude)')

    class Meta:
        model = AQIMeasurement
        fields = ['pollution', 'date_time', 'point', 'standard'] 

    def filter_by_standard(self, queryset, name, value):
        return queryset.filter(measurements__standard__description=value).distinct()
    
    def filter_by_coordinates(self, queryset, name, value):
        try:
            value = value.replace('(', '').replace(')', '').replace(' ', '')
            
            lat, lon = map(float, value.split(','))
            point = Point(lon, lat)

            points = AQIPoint.objects.filter(coordinates=point)

            return queryset.filter(point__in=points)
        
        except (ValueError, TypeError):
            return queryset.none() 
        
class StandardFilter(django_filters.FilterSet):

    class Meta: 
        model = AQIStandard
        fields = ['lower_limit', 'upper_limit', 'description'] 