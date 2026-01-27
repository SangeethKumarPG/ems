from django import forms
from .models import Booking
from django.utils import timezone

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['event_sub_type', 'date', 'venue', 'additional_details']
        widgets = {
            'event_sub_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Mehendi, Haldi'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'venue': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter venue location'}),
            'additional_details': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Any special requirements?'}),
        }

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if date < timezone.now().date():
            raise forms.ValidationError("Booking date cannot be in the past.")
        return date

class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email Address'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Your Message'}))

class EnquiryForm(forms.Form):
    full_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'E.g. John Doe'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'email@example.com'}))
    phone = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'placeholder': '+91 0000 000 000'}))
    event_interest = forms.ChoiceField(
        choices=[
            ('wedding', 'Wedding'),
            ('birthday', 'Birthday'),
            ('corporate', 'Corporate'),
            ('other', 'Other Celebration'),
        ],
        widget=forms.Select()
    )
    details = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows': 5, 'placeholder': "Tell us more about what you're looking for..."}))

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Simple digit validation
        clean_p = ''.join(filter(str.isdigit, phone))
        if len(clean_p) < 10:
            raise forms.ValidationError("Phone number must be at least 10 digits.")
        return phone
