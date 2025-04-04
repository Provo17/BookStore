from django.db import models
from books.models import Book
from users.models import User
from django.core.exceptions import ValidationError


class Sale(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="sales")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sales")
    quantity = models.PositiveIntegerField()
    sale_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} copies of {self.book.title} sold on {self.sale_date.strftime('%b %d, %Y at %I:%M %p')}"

    def clean(self):
        """
        Ensure there is enough stock for the sale.
        """
        if self.book.stock is None or self.book.stock < self.quantity:
            raise ValidationError("Not enough stock available for this book.")

    def save(self, *args, **kwargs):
        """
        Override save() to ensure stock is updated when a sale is made.
        """
        self.clean()  # Ensure validation runs before saving
        self.book.stock -= self.quantity
        self.book.save()
        super().save(*args, **kwargs)

    @staticmethod
    def update_book_quantity(book_id, quantity):
        """
        Update the sales count and reduce stock for a book.
        """
        try:
            book = Book.objects.get(id=book_id)

            if book.stock is None or book.stock < quantity:
                raise ValidationError("Not enough stock available.")

            book.stock -= quantity
            book.save()
            return f"Stock updated: {book.stock} remaining."

        except Book.DoesNotExist:
            raise ValidationError("Book does not exist.")

