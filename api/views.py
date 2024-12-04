from django.utils import timezone
from rest_framework import viewsets
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from rest_framework.permissions import IsAdminUser, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import CustomPagination
from .models import AQIStandard, AQIPoint, AQIMeasurement
from .filters import PointFilter, MeasurementFilter, StandardFilter
from .serializers import PointSerializer, MeasurementSerializer, StandardSerializer, CreateMeasurementSerializer
        
class PointViewSet(viewsets.ModelViewSet):
    queryset = AQIPoint.objects.all().order_by('id')
    serializer_class =  PointSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PointFilter
    pagination_class = CustomPagination
    
    def get_permissions(self):
        if self.request.method in ['GET']:
            return [AllowAny()]
        return [IsAdminUser()]

class MeasurementViewSet(viewsets.ModelViewSet):
    queryset = AQIMeasurement.objects.all().order_by('id')
    serializer_class = MeasurementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = MeasurementFilter
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.request.method in ['GET']:
            return [AllowAny()]
        return [IsAdminUser()]
    
    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update' or self.action == 'partial_update':
            return CreateMeasurementSerializer
        return MeasurementSerializer

    def create(self, request):
        lon = request.data.get('lon')
        lat = request.data.get('lat')
        pollution = request.data.get('pollution')
        noise = request.data.get('noise')
        date_time = request.data.get('date_time', timezone.now().isoformat())
        point_id = request.data.get('point_id')
           
        if not (lon and lat and pollution and noise):
            return Response({'error': 'Missing required parameters'}, status=400)

        if point_id:
            try:
                point = AQIPoint.objects.get(id=point_id)
            except AQIPoint.DoesNotExist:
                return Response({'error': 'Point not found'}, status=404)
        else:
            point, created = AQIPoint.objects.get_or_create(
                coordinates=Point(lon, lat)
            )

        standards = AQIStandard.objects.all()

        standard = None
        for st in standards:
            
            if ((st.lower_limit is None or pollution >= st.lower_limit) and
                (st.upper_limit is None or pollution < st.upper_limit)):
                standard = st
                break

        measurement = AQIMeasurement.objects.create(
            point=point,
            pollution=pollution,
            standard=standard,
            noise=noise,
            date_time=date_time
        )

        measurement_serializer = MeasurementSerializer(measurement)
        return Response({'message': 'Measurement added', 'data': measurement_serializer.data}, status=201)
    
    def update(self, request, pk=None, partial=False):
        measurement = self.get_object()

        lon = request.data.get('lon') 
        lat = request.data.get('lat')
        pollution = request.data.get('pollution')
        noise = request.data.get('noise')
        date_time = request.data.get('date_time', timezone.now().isoformat())
        point_id = request.data.get('point_id')
        

        if point_id:
            try:
                point = AQIPoint.objects.get(id=point_id)
            except AQIPoint.DoesNotExist:
                return Response({'error': 'Point not found'}, status=404)
        else:
            coordinates = Point(float(lon), float(lat)) if lon and lat else measurement.point.coordinates


            point, created = AQIPoint.objects.get_or_create(
                coordinates=coordinates
            )

        if pollution is not None:
            measurement.pollution = pollution
        if noise is not None:
            measurement.noise = noise

        measurement.date_time = date_time

        standard = None
        if pollution is not None:
            standards = AQIStandard.objects.all()
            for st in standards:
                if ((st.lower_limit is None or pollution >= st.lower_limit) and
                    (st.upper_limit is None or pollution < st.upper_limit)):
                    standard = st
                    break

        if standard is not None:
            measurement.standard = standard

        measurement.point = point
        measurement.save()

        measurement_serializer = MeasurementSerializer(measurement)

        return Response({'message': 'Measurement updated', 'data': measurement_serializer.data}, status=200)
    
class StandardViewSet(viewsets.ModelViewSet):
    queryset = AQIStandard.objects.all().order_by('id')
    serializer_class = StandardSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = StandardFilter
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.request.method in ['GET']:
            return [AllowAny()]
        return [IsAdminUser()]
    




