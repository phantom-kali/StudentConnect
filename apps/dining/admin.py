from django.contrib import admin
from .models import DiningHall, MenuItem, DiningHallReview

@admin.register(DiningHall)
class DiningHallAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'dining_hall', 'price', 'is_available')
    list_filter = ('dining_hall', 'is_available')

@admin.register(DiningHallReview)
class DiningHallReviewAdmin(admin.ModelAdmin):
    list_display = ('dining_hall', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')