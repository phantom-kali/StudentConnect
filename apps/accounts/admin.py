from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'is_student', 'is_premium', 'referral_code')
    list_filter = ('is_student', 'is_premium')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('bio', 'location', 'birth_date', 'profile_picture', 'is_premium', 'premium_until', 'referral_code', 'referred_by', 'referral_count')}),
    )
