from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'start_time', 'end_time', 'creator')
    list_filter = ('start_time', 'end_time', 'created_at')
    search_fields = ('title', 'description', 'location')
    filter_horizontal = ('attendees',)