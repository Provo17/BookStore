from django.shortcuts import render
from books.models import Book
def index(request):
    # Get the highest ranked books
    highest_ranked = Book.objects.filter(rating=5).order_by('title')[:8]
    # Fetch best sellers
    best_sellers = Book.objects.order_by('-total_sales')[:8]

    # Get the best book in each genre
    genres = Book.objects.values_list('genre', flat=True).distinct()  # Get all unique genres
    best_in_genre = {
        genre: Book.objects.filter(genre=genre).order_by('-rating', 'title').first()
        for genre in genres
    }

    context = {
        'highest_ranked': highest_ranked,
        'best_in_genre': best_in_genre,
        'best_sellers': best_sellers,
    }

    return render(request, 'bookstore/homepage.html', context)  # Include the 'bookstore/' prefix

