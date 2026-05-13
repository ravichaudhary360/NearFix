from django.db import models

# Create your models here.
# services/models.py
from django.db import models
from accounts.models import User

class Category(models.Model):
    name = models.CharField(max_length=100) # e.g., Plumber, Electrician
    image = models.ImageField(upload_to='categories/')

    def __str__(self):
        return self.name

class ProviderProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    hourly_rate = models.DecimalField(max_digits=6, decimal_places=2)
    is_available = models.BooleanField(default=True)
    rating = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.user.username} - {self.category.name}"
