from django.db import models
from django.utils.text import slugify


class Book(models.Model):
    GENRE_CHOICES = [
        ('FIC', 'Fiction'),
        ('NF', 'Non-Fiction'),
        ('MYST', 'Mystery'),
        ('SCI', 'Science'),
        ('FANT', 'Fantasy'),
        ('BIO', 'Biography'),
        ('HIST', 'History'),
        ('ROM', 'Romance'),
        ('CHILD', 'Children'),
        ('OTHER', 'Other'),
    ]

    AGE_RANGE_CHOICES = [
        ('0-3', '0-3 years'),
        ('4-7', '4-7 years'),
        ('8-12', '8-12 years'),
        ('13-18', '13-18 years'),
        ('18+', '18+ years'),
    ]

    slug = models.SlugField(unique=True, blank=True, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    publication_date = models.DateField()
    author = models.CharField(max_length=100)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    price = models.DecimalField(max_digits=6, decimal_places=2)
    genre = models.CharField(max_length=10, choices=GENRE_CHOICES, default='OTHER')
    isbn_13 = models.CharField(max_length=13, unique=True)
    publisher = models.CharField(max_length=100)
    pages = models.IntegerField()
    age_range = models.CharField(max_length=10, choices=AGE_RANGE_CHOICES, default='18+')
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    stock = models.IntegerField(default=0)
    total_sales = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        unique_slug = slugify(self.title)
        self.slug = unique_slug
        super().save(*args, **kwargs)

class Sale(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="sales")
    quantity = models.PositiveIntegerField()
    sale_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} copies of {self.book.title} sold on {self.sale_date}"

    @staticmethod
    def update_book_sales(book_id, quantity):
        """
        Update the sales count and reduce stock for a book.
        """
        book = Book.objects.get(id=book_id)
        book.stock -= quantity
        book.save()