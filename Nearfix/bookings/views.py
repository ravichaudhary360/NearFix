from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ProviderProfile, Booking, Review
from .models import Notification


CATEGORY_MAP = {
    'electrician':  {'name': 'Electrician',  'icon': '⚡'},
    'plumber':      {'name': 'Plumber',       'icon': '🔧'},
    'carpenter':    {'name': 'Carpenter',     'icon': '🪚'},
    'painter':      {'name': 'Painter',       'icon': '🎨'},
    'ac-repair':    {'name': 'AC Repair',     'icon': '❄️'},
    'cleaner':      {'name': 'Cleaner',       'icon': '🧹'},
    'mechanic':     {'name': 'Mechanic',      'icon': '🔩'},
    'pest-control': {'name': 'Pest Control',  'icon': '🐛'},
}


def providers_list(request):
    category = request.GET.get('category', '')
    city = request.GET.get('city', '')

    CATEGORY_MAP = {
        'electrician':  {'name': 'Electrician',  'icon': '⚡'},
        'plumber':      {'name': 'Plumber',       'icon': '🔧'},
        'carpenter':    {'name': 'Carpenter',     'icon': '🪚'},
        'painter':      {'name': 'Painter',       'icon': '🎨'},
        'ac-repair':    {'name': 'AC Repair',     'icon': '❄️'},
        'cleaner':      {'name': 'Cleaner',       'icon': '🧹'},
        'mechanic':     {'name': 'Mechanic',      'icon': '🔩'},
        'pest-control': {'name': 'Pest Control',  'icon': '🐛'},
    }

    CITY_CHOICES = [
        ('anupshahr',   'Anupshahr'),
        ('dibai',       'Dibai'),
        ('shikarpur',   'Shikarpur'),
        ('jahangirabad','Jahangirabad'),
    ]

    cat_info = CATEGORY_MAP.get(category, {'name': category.title(), 'icon': '🔍'})

    providers = ProviderProfile.objects.filter(is_available=True)

    if category:
        providers = providers.filter(trade__icontains=cat_info['name'])

    if city:
        providers = providers.filter(city=city)

    return render(request, 'bookings/providers_list.html', {
        'providers':     providers,
        'category':      category,
        'cat_info':      cat_info,
        'city':          city,
        'city_choices':  CITY_CHOICES,
    })


def provider_detail(request, pk):
    provider = get_object_or_404(ProviderProfile, pk=pk)
    reviews = Review.objects.filter(booking__provider=provider).order_by('-created_at')[:5]
    return render(request, 'bookings/provider_detail.html', {
        'provider': provider,
        'reviews': reviews,
    })




@login_required
def create_booking(request, provider_id):
    provider = get_object_or_404(ProviderProfile, pk=provider_id)

    if request.method == 'POST':
        description = request.POST.get('description', '')
        address     = request.POST.get('address', '')
        service     = request.POST.get('service_type', provider.trade)

        booking = Booking.objects.create(
            customer=request.user,
            provider=provider,
            service_type=service,
            description=description,
            address=address,
            status=Booking.STATUS_PENDING,
        )
# Provider ko notification
        Notification.objects.create(
    user=provider.user,
    title='New Booking Request! 🔔',
    message=f'{request.user.get_full_name()} ne {service} ke liye request bheja hai.',
    link=f'/dashboard/',
)
# Customer ko notification
        Notification.objects.create(
    user=request.user,
    title='Booking Sent! ✅',
    message=f'Aapka booking request {provider.user.get_full_name()} ko bheja gaya hai.',
    link=f'/bookings/{booking.pk}/',
)
        messages.success(request, f'Booking request sent to {provider.user.get_full_name()}!')
        return redirect('booking_detail', pk=booking.pk)

    return render(request, 'bookings/create_booking.html', {'provider': provider})


@login_required
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    return render(request, 'bookings/booking_detail.html', {'booking': booking})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'bookings/my_bookings.html', {'bookings': bookings})


@login_required
def provider_dashboard(request):
    try:
        profile = request.user.provider_profile
    except ProviderProfile.DoesNotExist:
        messages.error(request, 'Provider profile not found.')
        return redirect('home')

    pending   = Booking.objects.filter(provider=profile, status=Booking.STATUS_PENDING).order_by('-created_at')
    accepted  = Booking.objects.filter(provider=profile, status=Booking.STATUS_ACCEPTED).order_by('-created_at')
    completed = Booking.objects.filter(provider=profile, status=Booking.STATUS_COMPLETED).order_by('-created_at')

    return render(request, 'bookings/provider_dashboard.html', {
        'profile':   profile,
        'pending':   pending,
        'accepted':  accepted,
        'completed': completed,
    })


@login_required
def update_booking_status(request, pk, status):
    booking = get_object_or_404(Booking, pk=pk)

    allowed = [Booking.STATUS_ACCEPTED, Booking.STATUS_REJECTED,
               Booking.STATUS_ONGOING, Booking.STATUS_COMPLETED]
    if status in allowed:
        booking.status = status
        booking.save()
    
    status_messages = {
    'accepted': ('Booking Accepted! 🎉', f'{booking.provider.user.get_full_name()} ne aapki booking accept kar li!'),
    'rejected': ('Booking Rejected ❌', f'{booking.provider.user.get_full_name()} ne aapki booking reject kar di.'),
    'completed': ('Service Complete! ✅', f'Aapki {booking.service_type} service complete ho gayi. Review karo!'),
}
    if status in status_messages:
       Notification.objects.create(
        user=booking.customer,
        title=status_messages[status][0],
        message=status_messages[status][1],
        link=f'/bookings/{booking.pk}/',
    )
       messages.success(request, f'Booking status updated to {status}.')

    return redirect('provider_dashboard')

# yaha se addd karaa new code 
from .forms import ProviderRegistrationForm

@login_required
def provider_register(request):
    # Agar already provider hai toh dashboard pe bhejo
    if hasattr(request.user, 'provider_profile'):
        return redirect('provider_dashboard')
    
    if request.method == 'POST':
        form = ProviderRegistrationForm(request.POST)
        if form.is_valid():
            d = form.cleaned_data
            ProviderProfile.objects.create(
                user=request.user,
                trade=d['trade'],
                bio=d.get('bio', ''),
                experience_years=d['experience_years'],
                is_available=True,
            )
            messages.success(request, "Provider profile created successfully!")
            return redirect('provider_dashboard')
    else:
        form = ProviderRegistrationForm()
    
    return render(request, 'bookings/provider_register.html', {'form': form})

@login_required
def edit_provider_profile(request):
    try:
        profile = request.user.provider_profile
    except:
        return redirect('home')

    TRADE_CHOICES = [
        'Electrician', 'Plumber', 'Carpenter', 'Painter',
        'AC Repair', 'Cleaner', 'Mechanic', 'Pest Control',
        'Mason', 'Welder', 'CCTV Technician', 'Internet/WiFi Technician',
        'Washing Machine Repair', 'Refrigerator Repair', 'TV Repair',
        'Gardener', 'Security Guard', 'Driver', 'Cook', 'Other'
    ]

    if request.method == 'POST':
        profile.trade = request.POST.get('trade', profile.trade)
        profile.experience_years = int(request.POST.get('experience_years', 0))
        profile.bio = request.POST.get('bio', '')

        profile.is_available = request.POST.get('is_available') == 'on'
        profile.city = request.POST.get('city', profile.city)
        profile.save()

        request.user.first_name = request.POST.get('first_name', request.user.first_name)
        request.user.last_name = request.POST.get('last_name', request.user.last_name)
        request.user.phone = request.POST.get('phone', request.user.phone)

        # Photo upload handle karo
        if 'profile_photo' in request.FILES:
            request.user.profile_photo = request.FILES['profile_photo']

        request.user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('provider_dashboard')

    return render(request, 'bookings/edit_provider_profile.html', {
        'profile': profile,
        'trade_choices': TRADE_CHOICES,
    })
@login_required
def payment_page(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id, customer=request.user)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method', 'cash')
        amount = request.POST.get('amount', 0)
        booking.amount = amount
        booking.status = Booking.STATUS_COMPLETED
        booking.save()
        messages.success(request, 'Payment successful! Please rate your experience.')
        return redirect('review_page', booking_id=booking.pk)

    return render(request, 'bookings/payment.html', {'booking': booking})


@login_required
def review_page(request, booking_id):
    # booking = get_object_or_404(Booking, pk=booking_id, customer=request.user)
    booking = get_object_or_404(Booking, pk=booking_id)

    # Check if review already exists
    try:
        existing_review = booking.review
        messages.info(request, 'You have already reviewed this booking.')
        return redirect('my_bookings')
    except Review.DoesNotExist:
        pass

    if request.method == 'POST':
        rating = int(request.POST.get('rating', 5))
        comment = request.POST.get('comment', '')

        Review.objects.create(
            booking=booking,
            rating=rating,
            comment=comment,
        )

        # Update provider rating
        provider = booking.provider
        all_reviews = Review.objects.filter(booking__provider=provider)
        total = sum([r.rating for r in all_reviews])
        provider.rating = total / all_reviews.count()
        provider.total_reviews = all_reviews.count()
        provider.save()

        messages.success(request, 'Thank you for your review!')
        return redirect('my_bookings')

    return render(request, 'bookings/review.html', {'booking': booking})
@login_required
def notifications(request):
    notifs = request.user.notifications.all()
    # Sab read mark karo
    notifs.update(is_read=True)
    return render(request, 'bookings/notifications.html', {'notifications': notifs})


def unread_count(request):
    from django.http import JsonResponse
    if request.user.is_authenticated:
        count = request.user.notifications.filter(is_read=False).count()
        return JsonResponse({'count': count})
    return JsonResponse({'count': 0})