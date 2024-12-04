import csv
import os
from django.core.management.base import BaseCommand
from api.models import AQIMeasurement, AQIPoint, AQIStandard
from django.contrib.gis.geos import Point
from django.utils import timezone

class Command(BaseCommand):
    help = 'Import pollution data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='CSV file path')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']

        if not os.path.exists(csv_file_path):
            self.stderr.write(self.style.ERROR(f"File '{csv_file_path}' does not exist."))
            return

        with open(csv_file_path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                coordinates = Point(float(row['lon']), float(row['lat']))

                point, created = AQIPoint.objects.get_or_create(
                    coordinates=coordinates
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f"Added new point with id: {point.id}"))
                else:
                    self.stdout.write(self.style.WARNING(f"Point with id {point.id} already exists"))

                noise = float(row['noise'])
                pollution = float(row['pollution'])

                standards = AQIStandard.objects.all()

                standard = None
                for st in standards:
                    
                    if ((st.lower_limit is None or pollution >= st.lower_limit) and
                        (st.upper_limit is None or pollution < st.upper_limit)):
                        standard = st
                        break

                if not standard:
                    self.stdout.write(self.style.ERROR(f"No standard found for air quality index {pollution}"))

                AQIMeasurement.objects.create(
                    point=point,
                    pollution=pollution,
                    noise=noise,
                    standard=standard,
                    date_time=timezone.now()
                )

                self.stdout.write(self.style.SUCCESS(f"Added measurement for point {point.id}"))

        self.stdout.write(self.style.SUCCESS('Data import complete.'))
