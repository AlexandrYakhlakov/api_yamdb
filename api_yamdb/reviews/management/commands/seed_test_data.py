import csv
import os

from django.conf import settings
from django.core.management import BaseCommand
from django.utils import timezone

from reviews.models import (
    Category, Comment, Genre, Review, Title, User, TitleGenre
)


class Command(BaseCommand):
    DIRECTORY = f'{settings.BASE_DIR}/static/data/'
    MODEL_FILE = {
        User: 'users.csv',
        Category: 'category.csv',
        Genre: 'genre.csv',
        Title: 'titles.csv',
        TitleGenre: 'genre_title.csv',
        Review: 'review.csv',
        Comment: 'comments.csv',

    }

    def handle(self, *args, **kwargs):
        self.check_files()

        self.stdout.write(
            self.style.SUCCESS(f'{timezone.now()}. start: seed_test_data')
        )
        for model, file in self.MODEL_FILE.items():
            with open(f'{self.DIRECTORY}{file}', 'r',) as csv_file:
                try:
                    reader = csv.DictReader(csv_file, delimiter=',')
                    model.objects.bulk_create(
                        [model(**data) for data in reader]
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'{timezone.now()}. {e}')
                    )
        self.stdout.write(
            self.style.SUCCESS(f'{timezone.now()}. end: seed_test_data')
        )

    def check_files(self):
        self.stdout.write(
            self.style.SUCCESS(
                f'{timezone.now()}. start: check_files'
            )
        )
        file_not_found = []
        for file_name in self.MODEL_FILE.values():
            if not os.path.isfile(f'{self.DIRECTORY}{file_name}'):
                file_not_found.append(file_name)
        if file_not_found:
            self.stdout.write(
                self.style.ERROR(
                    f'{timezone.now()}. Файлы не найдены:{file_not_found}'
                )
            )
            raise FileNotFoundError()

        self.stdout.write(
            self.style.SUCCESS(
                f'{timezone.now()}. end: check_files'
            )
        )
