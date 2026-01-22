from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserRegisterForm(forms.ModelForm):
    # Mapping fields from the HTML template to Django form fields
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter your full name', 'id': 'name'}))
    phone = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number', 'id': 'phone'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Enter your address', 'id': 'address', 'rows': 3}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter your email address', 'id': 'email'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Choose a username', 'id': 'username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter a secure password', 'id': 'password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['name'] # Storing full name in first_name for simplicity or consider splitting
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                phone=self.cleaned_data['phone'],
                address=self.cleaned_data['address']
            )
        return user
