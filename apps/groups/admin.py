from django.contrib import admin
from .models import Group, GroupPost

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', 'description')
    filter_horizontal = ('members',)

@admin.register(GroupPost)
class GroupPostAdmin(admin.ModelAdmin):
    list_display = ('group', 'user', 'content', 'created_at')
    list_filter = ('created_at', 'group')
    search_fields = ('content', 'user__username', 'group__name')