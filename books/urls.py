from django.urls import path
from .views import book_detail, book_list
from . import views  # Import views from the books app

urlpatterns = [
    path('', book_list, name='book_list'),
    path('book/<int:pk>/', book_detail, name='book_detail'),
    path('', views.homepage, name='homepage'),  # Homepage route
    path('books/', views.book_list, name='book-list'),  # Example route for book list
]
