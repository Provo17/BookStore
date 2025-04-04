from django.shortcuts import get_object_or_404, render, redirect
from .models import Book, Review
from django.http import JsonResponse
from payments.models import Sale
from .forms import ReviewForm
from django.conf import settings
import stripe

def book_list(request):
    books = Book.objects.all()
    return render(request, 'bookstore/book_list.html', {'books': books})


def book_detail(request, book_id):  # ✅ Ensure the parameter matches urls.py
    book = get_object_or_404(Book, pk=book_id)
    reviews = book.reviews.all().order_by('-created_at')  # Show newest reviews first

    if request.method == "POST":
        if request.user.is_authenticated:
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.book = book
                review.user = request.user
                review.save()
                return redirect('book_detail', book_id=book.id)  # Refresh page after submission
        else:
            return redirect('login')  # Redirect non-authenticated users to login
    else:
        form = ReviewForm()

    return render(request, "bookstore/book_detail.html", {"book": book, "reviews": reviews, "form": form})



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
    query = request.GET.get('q', '').strip()
    results = Book.objects.filter(title__icontains=query) if query else []

    # If request is an AJAX call, return JSON data
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        results_data = [
            {
                'title': book.title,
                'author': book.author,
                'cover_image': book.cover_image.url if book.cover_image else "https://via.placeholder.com/150",
                'book_url': f"/books/book/{book.id}/"
            } for book in results
        ]
        return JsonResponse({'results': results_data})

    # If normal request, render the full search page
    return render(request, 'bookstore/search_results.html', {'query': query, 'results': results})



def payment_success(request):
    return render(request, "bookstore/payment_success.html")

def payment_cancelled(request):
    return render(request, "bookstore/payment_cancelled.html")
