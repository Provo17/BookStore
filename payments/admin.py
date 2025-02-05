from django.contrib import admin
from .models import Sale

@admin.register(Sale)
class SalesAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'quantity', 'sale_date')
    search_fields = ('book', 'user', 'quantity', 'sale_date')
    list_filter = ('book', 'user', 'quantity', 'sale_date')
    list_editable = ('quantity',)  # Allow stock updates directly from the admin