# your_app/management/commands/import_csv.py
import csv
from django.core.management.base import BaseCommand
from dimmer_matching.models import Dimmer


class Command(BaseCommand):
    help = 'Import products from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']

        with open(csv_file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Create and save product object
                product = Product(
                    name=row['name'],
                    description=row['description'],
                    price=row['price']
                )
                product.save()

        self.stdout.write(self.style.SUCCESS('CSV file imported successfully!'))
