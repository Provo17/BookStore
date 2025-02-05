from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'rating', 'price', 'publisher', 'publication_date')
    search_fields = ('title', 'author', 'isbn_13')
    list_filter = ('genre', 'rating', 'age_range', 'publication_date')