from django.core.management.base import BaseCommand
from api.models import AQIStandard

class Command(BaseCommand):
    help = 'Seeds the database with air quality index categorizations'

    def handle(self, *args, **kwargs):
        standards = [
            {"lower_limit": None, "upper_limit": 50, "description": "Low"},
            {"lower_limit": 51, "upper_limit": 150, "description": "Medium"},
            {"lower_limit": 151, "upper_limit": None, "description": "High"},
        ]

        for standard in standards:
            obj, created = AQIStandard.objects.get_or_create(
                lower_limit=standard["lower_limit"],
                upper_limit=standard["upper_limit"],
                description=standard["description"]
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Added air quality index standard: {obj.description}"))
            else:
                self.stdout.write(self.style.WARNING(f"Air quality index standard '{obj.description}' already exists."))
