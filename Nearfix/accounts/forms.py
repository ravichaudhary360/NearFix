from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class CustomerSignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Aarav', 'class': 'nf-input'}))
    last_name = forms.CharField(max_length=30, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Singh', 'class': 'nf-input'}))
    email = forms.EmailField(required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'you@example.com', 'class': 'nf-input'}))
    phone = forms.CharField(max_length=15, required=True,
        widget=forms.TextInput(attrs={'placeholder': '+91 98765 43210', 'class': 'nf-input'}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Min. 8 characters', 'class': 'nf-input'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password', 'class': 'nf-input'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        user.role = User.ROLE_CUSTOMER
        if commit:
            user.save()
        return user


class ProviderSignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Ramesh', 'class': 'nf-input'}))
    last_name = forms.CharField(max_length=30, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'Kumar', 'class': 'nf-input'}))
    email = forms.EmailField(required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'you@example.com', 'class': 'nf-input'}))
    phone = forms.CharField(max_length=15, required=True,
        widget=forms.TextInput(attrs={'placeholder': '+91 98765 43210', 'class': 'nf-input'}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Min. 8 characters', 'class': 'nf-input'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password', 'class': 'nf-input'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        user.role = User.ROLE_PROVIDER
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Email or phone',
            'class': 'nf-input',
            'autofocus': True,
        }))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••',
            'class': 'nf-input',
        }))
