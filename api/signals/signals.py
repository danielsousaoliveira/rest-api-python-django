from django.db.models.signals import post_save
from django.dispatch import receiver
from api.models import AQIStandard, AQIPoint, AQIMeasurement
from dateutil import parser
import logging
logger = logging.getLogger(__name__)

@receiver(post_save, sender=AQIStandard)
def update_points(sender, instance, **kwargs):
    
    for point in AQIPoint.objects.all():
        if instance.lower_limit <= point.pollution < instance.upper_limit:
            point.standard = instance
            point.save()

@receiver(post_save, sender=AQIMeasurement)
def update_point_stats(sender, instance, **kwargs):

    point = AQIPoint.objects.get(id=instance.point.id)
 
    point.total_number_measurements = AQIMeasurement.objects.filter(point=instance.point.id).count()

    if not point.last_measurement_date or instance.date_time > point.last_measurement_date:
        standard = instance.standard
        point.last_measurement_date = instance.date_time
        if standard:
            point.last_standard = standard.description

    point.save()

post_save.connect(update_point_stats, sender=AQIMeasurement)