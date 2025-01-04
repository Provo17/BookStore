from django.shortcuts import get_object_or_404, render
from .models import Book  # Ensure 'Book' is the correct model name

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'bookstore/book_detail.html', {'book': book})
