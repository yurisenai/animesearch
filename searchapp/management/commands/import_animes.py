from django.core.management.base import BaseCommand, CommandError
from searchapp.models import Anime  # Adjust 'searchapp' to your actual app name
import csv

class Command(BaseCommand):
    help = 'Import anime from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file to import.')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']

        try:
            with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    Anime.objects.update_or_create(
                        anime_id=row['anime_id'], 
                        defaults={
                            'name': row['name'],
                            'genre': row['genre'],
                            'type': row['type'],
                            'episodes': row.get('episodes'),
                            'rating': row.get('rating'),
                            'members': row.get('members'),
                            'image_url': row.get('image_url', '')
                        }
                    )
            self.stdout.write(self.style.SUCCESS(f'Successfully imported data from {csv_file_path}'))
        except FileNotFoundError:
            raise CommandError(f'File "{csv_file_path}" does not exist.')
