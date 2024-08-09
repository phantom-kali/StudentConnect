from django.contrib import admin
from .models import Story, StoryView

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'caption', 'created_at', 'expires_at')
    list_filter = ('created_at', 'expires_at')

@admin.register(StoryView)
class StoryViewAdmin(admin.ModelAdmin):
    list_display = ('story', 'viewer', 'viewed_at')
    list_filter = ('viewed_at',)