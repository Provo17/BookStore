from django.urls import path
from .views import book_detail, book_list, record_sale, books_by_genre, search_books


urlpatterns = [
    path('', book_list, name='book_list'),
    path('book/<int:book_id>/', book_detail, name='book_detail'),  # ✅ Ensure this format
    path('books/', book_list, name='book-list'),  # Example route for book list
    path('<int:book_id>/record-sale/', record_sale, name='record_sale'),  # Book sale recording
    path('genre/<str:genre>/', books_by_genre, name="books_by_genre"),
    path('search/', search_books, name='search_books'),
]

