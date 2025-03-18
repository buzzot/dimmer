import os
import django

# ✅ Step 1: Ensure Django knows where to find settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dimmer_test.settings')  # Update if your project name is different
django.setup()

# ✅ Step 2: Import models *after* Django is set up
from dimmer_test.dimmer_matching.models import Dimmer

import csv
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Import dimmers from a CSV file'

    def add_arguments(self, parser):
        # Adding an argument for the file path
        parser.add_argument('csv_file', type=str, help="Path to the CSV file")

    def handle(self, *args, **kwargs):
        # Getting the file path from the command argument
        csv_file = kwargs['csv_file']

        # Open the CSV file and read data
        try:
            with open(csv_file, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                # Iterate over each row in the CSV
                for row in reader:
                    # Extracting fields
                    dim_number = row['dim_number']
                    brand = row['brand']
                    series = row['series']
                    model = row['model']
                    dimming_protocol = row['dimming_protocol']
                    manufacturer_url = row['manufacturer_url']

                    # Create a Dimmer instance and save it to the database

                    Dimmer.objects.create(
                        dim_number=dim_number,
                        brand=brand,
                        series=series,
                        model=model,
                        dimming_protocol=dimming_protocol,
                        manufacturer_url=manufacturer_url
                    )

                self.stdout.write(self.style.SUCCESS(f'Successfully imported dimmers from {csv_file}'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File {csv_file} not found"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))
