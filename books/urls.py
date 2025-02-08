from django.urls import path
from .views import book_detail, book_list, record_sale, books_by_genre
from . import views  # Import views from the books app

urlpatterns = [
    path('', book_list, name='book_list'),
    path('book/<int:pk>/', book_detail, name='book_detail'),
    path('books/', views.book_list, name='book-list'),  # Example route for book list
    path('<int:book_id>/record-sale/', record_sale, name='record_sale'),  # Book sale recording
    path('genre/<str:genre>/', books_by_genre, name="books_by_genre"),
]

