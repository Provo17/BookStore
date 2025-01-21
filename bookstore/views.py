from django.shortcuts import render
from books.models import Book
def index(request):
    books = Book.objects.filter(rating=5).order_by('title')[:8]
    return render(request, 'bookstore/homepage.html', {'books': books})  # Include the 'bookstore/' prefix
