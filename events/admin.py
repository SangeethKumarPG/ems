from django.contrib import admin
from .models import Event, Booking

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'price', 'created_at')
    search_fields = ('title', 'description', 'category')
    list_filter = ('category', 'created_at')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'event_type', 'date', 'status', 'created_at')
    list_filter = ('status', 'date')
    search_fields = ('user__username', 'event_type', 'venue')
