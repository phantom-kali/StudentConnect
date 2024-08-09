from django.contrib import admin
from .models import MarketplaceItem

@admin.register(MarketplaceItem)
class MarketplaceItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'seller', 'created_at')
    list_filter = ('created_at', 'seller')
    search_fields = ('title', 'description')