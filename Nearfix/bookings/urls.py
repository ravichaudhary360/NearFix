from django.urls import path
from . import views

urlpatterns = [
    path('providers/', views.providers_list, name='providers_list'),
    path('providers/<int:pk>/', views.provider_detail, name='provider_detail'),
    path('providers/<int:provider_id>/book/', views.create_booking, name='create_booking'),
    path('bookings/', views.my_bookings, name='my_bookings'),
    path('bookings/<int:pk>/', views.booking_detail, name='booking_detail'),
    path('dashboard/', views.provider_dashboard, name='provider_dashboard'),
    path('bookings/<int:pk>/status/<str:status>/', views.update_booking_status, name='update_booking_status'),
    path('provider/register/', views.provider_register, name='provider_register'), 
    path('provider/edit/', views.edit_provider_profile, name='edit_provider_profile'),
    path('bookings/<int:booking_id>/payment/', views.payment_page, name='payment_page'),
    path('bookings/<int:booking_id>/review/', views.review_page, name='review_page'),
    path('notifications/', views.notifications, name='notifications'),
    path('notifications/count/', views.unread_count, name='unread_count'),
]