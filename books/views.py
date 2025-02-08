from django.shortcuts import get_object_or_404, render
from .models import Book
from django.http import JsonResponse
from payments.models import Sale
def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookstore/book_list.html', {'books': books})


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'bookstore/book_detail.html', {'book': book})


def record_sale(request, book_id):
    """
    Record a sale for a book.
    """
    # Ensure the user is logged in
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'You must be logged in to purchase a book'}, status=403)

    book = get_object_or_404(Book, id=book_id)
    quantity = int(request.POST.get('quantity', 1))

    # Ensure sufficient stock
    if book.stock < quantity:
        return JsonResponse({'error': 'Not enough stock available'}, status=400)

    # Create Sale record with user
    Sale.objects.create(book=book, user=request.user, quantity=quantity)

    # Update Book's total sales and stock
    book.stock -= quantity
    book.save()

    return JsonResponse({'success': 'Sale recorded successfully'})

def books_by_genre(request, genre):
    """Display books filtered by genre"""
    books = Book.objects.filter(genre=genre)
    return render(request, "bookstore/book_list.html", {"books": books, "genre": genre})

GENRE_MAPPING = {
    'FIC': 'Fiction',
    'NF': 'Non-Fiction',
    'MYST': 'Mystery',
    'SCI': 'Science',
    'FANT': 'Fantasy',
    'BIO': 'Biography',
    'HIST': 'History',
    'ROM': 'Romance',
    'CHILD': 'Children',
    'OTHER': 'Other',
}

def books_by_genre(request, genre):
    """ Display books filtered by genre """
    if genre not in GENRE_MAPPING:
        return render(request, "bookstore/book_list.html", {"books": [], "genre": "Unknown Genre"})

    books = Book.objects.filter(genre=genre)  # Match against database genre values
    return render(request, "bookstore/book_list.html", {"books": books, "genre": GENRE_MAPPING[genre]})

def search_books(request):
    query = request.GET.get('q', '')
    results = Book.objects.filter(title__icontains=query) if query else []

    # Assign a default image if cover_image is missing
    for book in results:
        if not book.cover_image:
            book.cover_image_url = "https://via.placeholder.com/180x250"
        else:
            book.cover_image_url = book.cover_image.url

    return render(request, 'bookstore/search_results.html', {'query': query, 'results': results})
