from django.contrib.gis.db import models
from django.utils import timezone
from django.contrib.gis.geos import Point

class AQIStandard(models.Model):
    id = models.AutoField(primary_key=True)
    lower_limit = models.FloatField(null=True)
    upper_limit = models.FloatField(null=True)
    description = models.CharField(max_length=50)

    def __str__(self):
        return f"Air Quality Index Standard {self.id}: {self.description} ({self.lower_limit} - {self.upper_limit})"
class AQIPoint(models.Model):
    id = models.AutoField(primary_key=True)
    coordinates = models.PointField(default=Point(0, 0)) 
    total_number_measurements = models.IntegerField(default=0)
    last_standard = models.CharField(max_length=50, null=True)
    last_measurement_date = models.DateTimeField(null=True)
    def __str__(self):
        return f"Point {self.id} ({self.coordinates})"

class AQIMeasurement(models.Model):
    id = models.AutoField(primary_key=True)
    point = models.ForeignKey(AQIPoint, on_delete=models.CASCADE, related_name='measurements', default=1)
    pollution = models.FloatField()
    noise = models.FloatField()
    standard = models.ForeignKey(AQIStandard, on_delete=models.CASCADE, default=1, null=True)
    date_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Measurement id {self.id} for point {self.point} at {self.date_time}"
