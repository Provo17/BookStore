from django.urls import path
from .views import book_detail

urlpatterns = [
    path('book/<int:pk>/', book_detail, name='book_detail'),
]
