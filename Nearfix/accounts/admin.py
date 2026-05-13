from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'get_full_name', 'email', 'phone', 'role', 'is_verified', 'is_active', 'date_joined']
    list_filter = ['role', 'is_verified', 'is_active', 'date_joined']
    search_fields = ['username', 'first_name', 'last_name', 'email', 'phone']
    list_editable = ['role', 'is_verified', 'is_active']
    ordering = ['-date_joined']

    fieldsets = UserAdmin.fieldsets + (
        ('NearFix Info', {
            'fields': ('role', 'phone', 'is_verified', 'profile_photo', 'created_at')
        }),
    )
    readonly_fields = ['created_at']

    def get_full_name(self, obj):
        return obj.get_full_name() or '—'
    get_full_name.short_description = 'Full Name'