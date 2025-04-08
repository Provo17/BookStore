from django.urls import path
from . import views

from django.urls import path, include
from .views import signup, user_account, custom_login, purchase_history, edit_account

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('account/', user_account, name='user_account'),

    # ✅ Include Django's built-in authentication URLs (including logout)
    path('login/', custom_login, name='login'),
    path('account/history/', purchase_history, name='purchase_history'),
    path('account/edit/', edit_account, name='edit_account'),
]
