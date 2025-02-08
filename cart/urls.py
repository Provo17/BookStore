from django.urls import path
from .views import add_to_cart, cart_view, remove_from_cart, update_cart, checkout

urlpatterns = [
    path("", cart_view, name="cart_view"),
    path("add/<int:book_id>/", add_to_cart, name="add_to_cart"),
    path("remove/<int:book_id>/", remove_from_cart, name="remove_from_cart"),
    path("update/<int:book_id>/", update_cart, name="update_cart"),
    path("checkout/", checkout, name="checkout"),
]
