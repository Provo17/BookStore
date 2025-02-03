from django.db import models
from books.models import Book
from users.models import User

class Sale(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="sales")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sales")
    quantity = models.PositiveIntegerField()
    sale_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} copies of {self.book.title} sold on {self.sale_date}"

    @staticmethod
    def update_book_quantity(book_id, quantity):
        """
        Update the sales count and reduce stock for a book.
        """
        book = Book.objects.get(id=book_id)
        book.stock -= quantity
        book.save()
