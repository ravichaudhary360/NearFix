from django.db import models
from accounts.models import User


CITY_CHOICES = [
    ('anupshahr', 'Anupshahr'),
    ('dibai', 'Dibai'),
    ('shikarpur', 'Shikarpur'),
    ('jahangirabad', 'Jahangirabad'),
]

class ProviderProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='provider_profile')
    trade = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    experience_years = models.IntegerField(default=0)
    rating = models.FloatField(default=0.0)
    total_reviews = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    city = models.CharField(max_length=50, choices=CITY_CHOICES, default='anupshahr')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} — {self.trade}"


class Booking(models.Model):
    STATUS_PENDING   = 'pending'
    STATUS_ACCEPTED  = 'accepted'
    STATUS_REJECTED  = 'rejected'
    STATUS_ONGOING   = 'ongoing'
    STATUS_COMPLETED = 'completed'

    STATUS_CHOICES = [
        (STATUS_PENDING,   'Pending'),
        (STATUS_ACCEPTED,  'Accepted'),
        (STATUS_REJECTED,  'Rejected'),
        (STATUS_ONGOING,   'Ongoing'),
        (STATUS_COMPLETED, 'Completed'),
    ]

    customer        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings_as_customer')
    provider        = models.ForeignKey(ProviderProfile, on_delete=models.CASCADE, related_name='bookings')
    service_type    = models.CharField(max_length=100)
    description     = models.TextField(blank=True)
    status          = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    address         = models.TextField(blank=True)
    scheduled_at    = models.DateTimeField(null=True, blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    amount          = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"Booking #{self.id} — {self.customer.username} → {self.provider}"


class Review(models.Model):
    booking  = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    rating   = models.IntegerField(default=5)
    comment  = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for Booking #{self.booking.id} — {self.rating}⭐"
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.user.username} — {self.title}"

    class Meta:
        ordering = ['-created_at']