from django.urls import path
from .views import add_to_cart, cart_view, remove_from_cart, update_cart, create_checkout_session, payment_cancelled, payment_success, stripe_webhook

urlpatterns = [
    path("", cart_view, name="cart_view"),
    path("add/<int:book_id>/", add_to_cart, name="add_to_cart"),
    path("remove/<int:book_id>/", remove_from_cart, name="remove_from_cart"),
    path("update/<int:book_id>/", update_cart, name="update_cart"),
    path("create_checkout_session/", create_checkout_session, name="create_checkout_session"),  # ✅ Checkout session
    path("payment-success/", payment_success, name="payment_success"),
    path("payment-cancelled/", payment_cancelled, name="payment_cancelled"),
    path("webhook/", stripe_webhook, name="stripe_webhook"),
]
