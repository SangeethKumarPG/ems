from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    CATEGORY_CHOICES = [
        ('wedding', 'Wedding'),
        ('birthday', 'Birthday'),
        ('corporate', 'Corporate'),
        ('engagement', 'Engagement'),
        ('haldi', 'Haldi'),
        ('mehendi', 'Mehendi'),
        ('hindu_wedding', 'Hindu Wedding'),
        ('muslim_wedding', 'Muslim Wedding'),
        ('christian_wedding', 'Christian Wedding'),
        ('beach_wedding', 'Beach Wedding'),
        ('other', 'Other'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image_url = models.URLField(blank=True, help_text="External URL for the image")
    image = models.ImageField(upload_to='events/', blank=True, null=True, help_text="Upload image (optional)")
    features = models.TextField(blank=True, help_text="Features separated by newlines")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event_type = models.CharField(max_length=100, help_text="Type of event (e.g. Wedding, Birthday)")
    event_sub_type = models.CharField(max_length=100, blank=True, help_text="e.g. Mehendi, Haldi")
    date = models.DateField()
    venue = models.CharField(max_length=200)
    additional_details = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.event_type} on {self.date}"
