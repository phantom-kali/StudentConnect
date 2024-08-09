from django.contrib import admin
from .models import Post, Comment, ReportOption, Report

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'created_at', 'view_count')
    list_filter = ('created_at',)
    search_fields = ('content', 'user__username')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'content', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'user__username')

@admin.register(ReportOption)
class ReportOptionAdmin(admin.ModelAdmin):
    list_display = ('reason',)

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'reason', 'created_at')
    list_filter = ('created_at', 'reason')
    search_fields = ('user__username', 'post__content')