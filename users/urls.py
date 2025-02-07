from django.urls import path
from . import views

from django.urls import path, include
from .views import signup, user_account, custom_login, purchase_history

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('account/', user_account, name='user_account'),

    # ✅ Include Django's built-in authentication URLs (including logout)
    path('', include('django.contrib.auth.urls')),
    path('login/', custom_login, name='login'),
    path('account/history/', purchase_history, name='purchase_history'),
]
