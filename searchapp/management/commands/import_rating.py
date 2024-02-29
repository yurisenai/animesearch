from django.core.management.base import BaseCommand, CommandError
from searchapp.models import AnimeRating  # Adjust 'searchapp' to your actual app name
import csv
from django.db import transaction

class Command(BaseCommand):
    help = 'Import anime from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file to import.')

    def handle(self, *args, **kwargs):
        csv_file_path = kwargs['csv_file']

        try:
            with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                anime_ratings_to_create = []

                for row in reader:
                    anime_ratings_to_create.append(AnimeRating(
                        anime_id=row['anime_id'],
                        user_id=row['user_id'],
                        rating=row['rating'],
                    ))

                # Use a transaction to wrap the bulk create for efficiency and safety
                with transaction.atomic():
                    AnimeRating.objects.bulk_create(anime_ratings_to_create, batch_size=1000) # Adjust batch_size as needed

            self.stdout.write(self.style.SUCCESS(f'Successfully imported data from {csv_file_path}'))
        except FileNotFoundError:
            raise CommandError(f'File "{csv_file_path}" does not exist.')
