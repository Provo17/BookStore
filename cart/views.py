from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart
from books.models import Book
from payments.models import Sale

@login_required
def add_to_cart(request, book_id):
    """ Add a book to the cart """
    book = get_object_or_404(Book, id=book_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, book=book)

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    messages.success(request, f"{book.title} added to cart!")
    return redirect("cart_view")


@login_required
def cart_view(request):
    """View the user's shopping cart"""
    cart_items = Cart.objects.filter(user=request.user)

    # Calculate total price for each item
    for item in cart_items:
        item.total_price = item.book.price * item.quantity  # Add total price to each item

    total_price = sum(item.book.price * item.quantity for item in cart_items)

    return render(request, "bookstore/cart.html", {"cart_items": cart_items, "total_price": total_price})

@login_required
def remove_from_cart(request, book_id):
    """ Remove a book from the cart """
    cart_item = get_object_or_404(Cart, user=request.user, book_id=book_id)
    cart_item.delete()

    messages.success(request, "Item removed from cart.")
    return redirect("cart_view")


@login_required
def update_cart(request, book_id):
    """ Update quantity of a book in the cart """
    cart_item = get_object_or_404(Cart, user=request.user, book_id=book_id)
    new_quantity = int(request.POST.get("quantity", 1))

    if new_quantity > 0:
        cart_item.quantity = new_quantity
        cart_item.save()
    else:
        cart_item.delete()

    return redirect("cart_view")

@login_required
def checkout(request):
    """ Process checkout and finalize purchases """
    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items:
        messages.error(request, "Your cart is empty.")
        return redirect("cart_view")

    for item in cart_items:
        if item.book.stock < item.quantity:
            messages.error(request, f"Not enough stock for {item.book.title}.")
            return redirect("cart_view")

    for item in cart_items:
        Sale.objects.create(
            user=request.user,
            book=item.book,
            quantity=item.quantity
        )
        item.book.stock -= item.quantity
        item.book.save()

    cart_items.delete()

    messages.success(request, "Purchase successful!")
    return redirect("purchase_history")