from rest_framework import serializers
from api.models import AQIPoint, AQIMeasurement, AQIStandard

class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = AQIPoint
        fields = '__all__'

class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = AQIMeasurement
        fields = '__all__'

class StandardSerializer(serializers.ModelSerializer):
    class Meta:
        model = AQIStandard
        fields = '__all__'

class CreateMeasurementSerializer(serializers.Serializer):
    lon = serializers.FloatField()
    lat = serializers.FloatField()
    speed = serializers.FloatField()
    date_time = serializers.DateTimeField(required=False)
    pointId = serializers.IntegerField(required=False)