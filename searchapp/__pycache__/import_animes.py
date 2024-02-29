from django.core.management.base import BaseCommand
import csv
from searchapp.models import Anime  # Adjust 'yourapp' to your actual app name

class Command(BaseCommand):
    help = 'Import anime from a CSV file into the Anime model'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The CSV file path')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Anime.objects.create(
                    anime_id=row.get('anime_id'),
                    name=row.get('name'),
                    genre=row.get('genre'),
                    type=row.get('type'),
                    episodes=row.get('episodes'),
                    rating=row.get('rating'),
                    members=row.get('members'),
                    image_url=row.get('image_url', '')
                )
        self.stdout.write(self.style.SUCCESS('Successfully imported anime data'))
