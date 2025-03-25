from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, CartItem
from books.models import Book
from payments.models import Sale
from django.conf import settings
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart = request.session.get("cart", {})  # Get existing cart

    if str(book_id) in cart:
        cart[str(book_id)]["quantity"] += 1
    else:
        # Convert Decimal to float so it's JSON serializable
        cart[str(book_id)] = {"quantity": 1, "price": float(book.price)}

    request.session["cart"] = cart  # Save updated cart
    request.session.modified = True  # Mark session as modified

    print("Cart Updated:", request.session["cart"])  # Debugging log

    messages.success(request, f"Added {book.title} to cart!")
    return redirect("cart_view")  # Redirect to cart page



@login_required
def cart_view(request):
    session_cart = request.session.get("cart", {})
    cart_items = []
    total_price = 0

    # Iterate over the session cart and fetch book details from the database
    for book_id, item in session_cart.items():
        book = get_object_or_404(Book, id=book_id)
        quantity = item.get("quantity", 0)
        # You can use the book.price from the DB or the stored price from the session
        item_total = book.price * quantity
        total_price += item_total

        cart_items.append({
            "book": book,
            "quantity": quantity,
            "total_price": item_total,
        })

    return render(request, "bookstore/cart.html", {
        "cart_items": cart_items,
        "total_price": total_price,
        "STRIPE_PUBLISHABLE_KEY": settings.STRIPE_PUBLISHABLE_KEY,
    })



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

stripe.api_key = settings.STRIPE_SECRET_KEY  # Set Stripe API Key

@csrf_exempt
def create_checkout_session(request):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': 'T-Shirt'},
                'unit_amount': 2000,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='https://yourdomain.com/success',
        cancel_url='https://yourdomain.com/cancel',
    )
    return JsonResponse({'sessionId': session.id})


def payment_success(request):
    return render(request, "bookstore/payment_success.html")

def payment_cancelled(request):
    return render(request, "bookstore/payment_cancelled.html")


@csrf_exempt
def stripe_webhook(request):
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET  # Set this in your settings.py
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError as e:
        return HttpResponse(status=400)  # Invalid payload
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)  # Invalid signature

    # ✅ Handle the payment success event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print("✅ Payment confirmed for session:", session["id"])
        # TODO: Update your order in the database here

    return HttpResponse(status=200)
