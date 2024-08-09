from django.contrib import admin
from .models import Confession

@admin.register(Confession)
class ConfessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'created_at')
