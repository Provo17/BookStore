import random
from django.core.management.base import BaseCommand
from faker import Faker
from books.models import Book

class Command(BaseCommand):
    help = 'Load mock book data into the database'

    def handle(self, *args, **kwargs):
        # Initialize Faker
        fake = Faker()

        # Define constants for mock data
        GENRE_CHOICES = ['FIC', 'NF', 'MYST', 'SCI', 'FANT', 'BIO', 'HIST', 'ROM', 'CHILD', 'OTHER']
        AGE_RANGE_CHOICES = ['0-3', '4-7', '8-12', '13-18', '18+']

        # Generate and save mock data
        for _ in range(50):  # Adjust the range for the number of records you want
            title = fake.sentence(nb_words=4).rstrip('.')
            Book.objects.create(
                slug=fake.slug(title),
                title=title,
                description=fake.text(max_nb_chars=200),
                publication_date=fake.date_between(start_date='-10y', end_date='today'),
                author=fake.name(),
                rating=random.randint(1, 5),
                price=round(random.uniform(5.0, 50.0), 2),
                genre=random.choice(GENRE_CHOICES),
                isbn_13=fake.isbn13(separator=''),
                publisher=fake.company(),
                pages=random.randint(100, 1000),
                age_range=random.choice(AGE_RANGE_CHOICES),
                cover_image=None,  # Leave blank or provide a default image
                stock=random.randint(0, 100),
            )

        self.stdout.write(self.style.SUCCESS('Mock book data successfully loaded!'))