from django import forms
from .models import ProviderProfile

TRADE_CHOICES = [
    ('Electrician', 'Electrician'),
    ('Plumber', 'Plumber'),
    ('Carpenter', 'Carpenter'),
    ('Painter', 'Painter'),
    ('AC Repair', 'AC Repair'),
    ('Cleaner', 'Cleaner'),
    ('Mechanic', 'Mechanic'),
    ('Pest Control', 'Pest Control'),
]

class ProviderRegistrationForm(forms.Form):
    trade = forms.ChoiceField(choices=TRADE_CHOICES)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    experience_years = forms.IntegerField(min_value=0, max_value=50)