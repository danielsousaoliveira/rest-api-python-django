from django.contrib import admin
from .models import AQIPoint, AQIMeasurement, AQIStandard

@admin.register(AQIPoint)
class AQIPointAdmin(admin.ModelAdmin):
    list_display = ('id', 'coordinates', 'total_number_measurements', 'last_standard', 'last_measurement_date')

@admin.register(AQIMeasurement)
class MeasurementAdmin(admin.ModelAdmin):
    list_display = ('id', 'point', 'pollution', 'noise', 'date_time', 'standard')

@admin.register(AQIStandard)
class StandardAdmin(admin.ModelAdmin):
    list_display = ('id', 'lower_limit', 'upper_limit', 'description')