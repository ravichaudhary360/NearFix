from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomerSignupForm, ProviderSignupForm, LoginForm
from .models import User


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name}!')
            # Provider hain toh dashboard pe bhejo
            if user.role == User.ROLE_PROVIDER:
                return redirect('provider_dashboard')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials. Please try again.')

    return render(request, 'accounts/login.html', {'form': form, 'active': 'login'})


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    role = request.GET.get('role', 'customer')
    customer_form = CustomerSignupForm()
    provider_form = ProviderSignupForm()

    if request.method == 'POST':
        role = request.POST.get('role', 'customer')

        if role == 'provider':
            form = ProviderSignupForm(request.POST)
        else:
            form = CustomerSignupForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            # Provider ka ProviderProfile automatically banao
            if user.role == User.ROLE_PROVIDER:
                from bookings.models import ProviderProfile
                trade = request.POST.get('trade', 'General Service')
                ProviderProfile.objects.create(
                    user=user,
                    trade=trade,
                    is_available=True,
                )
                messages.success(request, f'Welcome to NearFix, {user.first_name}! Complete your profile.')
                return redirect('provider_dashboard')

            messages.success(request, f'Account created! Welcome to NearFix, {user.first_name}!')
            return redirect('home')
        else:
            if role == 'provider':
                provider_form = form
            else:
                customer_form = form
            messages.error(request, 'Please fix the errors below.')

    return render(request, 'accounts/login.html', {
        'customer_form': customer_form,
        'provider_form': provider_form,
        'active': 'signup',
        'selected_role': role,
    })


def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})


def home_view(request):
    from bookings.models import ProviderProfile
    query = request.GET.get('q', '')
    city = request.GET.get('city', '')

    providers = None
    if query or city:
        providers = ProviderProfile.objects.filter(is_available=True)
        if query:
            providers = providers.filter(trade__icontains=query)
        if city:
            providers = providers.filter(city=city)

    return render(request, 'home.html', {
        'query': query,
        'city': city,
        'providers': providers,
    })

@login_required
def customer_profile(request):
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', request.user.first_name)
        request.user.last_name = request.POST.get('last_name', request.user.last_name)
        request.user.phone = request.POST.get('phone', request.user.phone)
        if 'profile_photo' in request.FILES:
            request.user.profile_photo = request.FILES['profile_photo']
        request.user.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('customer_profile')
    return render(request, 'accounts/customer_profile.html')