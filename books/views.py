from django.shortcuts import get_object_or_404, render
from .models import Book, Sale
from django.http import JsonResponse

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
    book = get_object_or_404(Book, id=book_id)
    quantity = int(request.POST.get('quantity', 1))

    # Ensure sufficient stock
    if book.stock < quantity:
        return JsonResponse({'error': 'Not enough stock available'}, status=400)

    # Create Sale record
    Sale.objects.create(book=book, quantity=quantity)

    # Update Book's total sales and stock
    book.total_sales += quantity
    book.stock -= quantity
    book.save()

    return JsonResponse({'success': 'Sale recorded successfully'})

