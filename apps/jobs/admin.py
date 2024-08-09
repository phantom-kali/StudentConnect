from django.contrib import admin
from .models import Job, Application

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'poster', 'created_at')
    list_filter = ('created_at', 'deadline')
    search_fields = ('title', 'company', 'description')

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'created_at')
    list_filter = ('created_at',)
