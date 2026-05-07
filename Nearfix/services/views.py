from django.shortcuts import render

# Create your views here.
# services/views.py
from django.shortcuts import render
from .models import ProviderProfile
import math

# Helper function: Haversine Formula
def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371.0 # Earth radius in kilometers
    
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c
    return distance

# Main View for the Home Page
def home(request):
    # For testing, let's assume the user is at these coordinates (e.g., center of a city)
    user_lat = 28.6139 
    user_lon = 77.2090
    max_distance_km = 5.0 # Show providers within 5km

    all_providers = ProviderProfile.objects.filter(is_available=True)
    nearby_providers = []

    for provider in all_providers:
        if provider.user.latitude and provider.user.longitude:
            dist = calculate_distance(user_lat, user_lon, provider.user.latitude, provider.user.longitude)
            if dist <= max_distance_km:
                provider.distance = round(dist, 1) # Add distance attribute for the HTML template
                nearby_providers.append(provider)

    context = {
        'providers': nearby_providers
    }
    return render(request, 'services/home.html', context)

