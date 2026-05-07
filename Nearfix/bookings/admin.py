from django.contrib import admin
from .models import ProviderProfile, Booking, Review, Notification


@admin.register(ProviderProfile)
class ProviderProfileAdmin(admin.ModelAdmin):
    list_display = ['get_name', 'trade', 'city', 'rating', 'total_reviews', 'experience_years', 'is_available', 'created_at']
    list_filter = ['trade', 'city', 'is_available']
    search_fields = ['user__first_name', 'user__last_name', 'user__email', 'trade']
    list_editable = ['is_available']
    ordering = ['-created_at']

    def get_name(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_name.short_description = 'Provider Name'


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_customer', 'get_provider', 'service_type', 'status', 'address', 'amount', 'created_at']
    list_filter = ['status', 'service_type', 'created_at']
    search_fields = ['customer__first_name', 'customer__email', 'provider__user__first_name', 'service_type']
    list_editable = ['status']
    ordering = ['-created_at']
    readonly_fields = ['created_at']

    def get_customer(self, obj):
        return obj.customer.get_full_name() or obj.customer.username
    get_customer.short_description = 'Customer'

    def get_provider(self, obj):
        return obj.provider.user.get_full_name() or obj.provider.user.username
    get_provider.short_description = 'Provider'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_booking', 'rating', 'comment', 'created_at']
    list_filter = ['rating']
    search_fields = ['booking__customer__first_name', 'comment']
    ordering = ['-created_at']

    def get_booking(self, obj):
        return f"Booking #{obj.booking.id} — {obj.booking.customer.username}"
    get_booking.short_description = 'Booking'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_user', 'title', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['user__username', 'title', 'message']
    list_editable = ['is_read']
    ordering = ['-created_at']

    def get_user(self, obj):
        return obj.user.get_full_name() or obj.user.username
    get_user.short_description = 'User'