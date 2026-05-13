from django.urls import path
from . import views

urlpatterns = [
    # Yeh blank path ('') views.home ko point karega
    path('', views.home, name='home'),
]