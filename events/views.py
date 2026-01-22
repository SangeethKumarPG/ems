from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Event, Booking
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def home(request):
    events = Event.objects.all()
    return render(request, 'users/home.html', {'events': events})

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.html'
    context_object_name = 'event'

@login_required
def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        event_sub_type = request.POST.get('event_sub_type', '')
        date = request.POST.get('date')
        venue = request.POST.get('venue')
        additional_details = request.POST.get('additional_details', '')
        
        Booking.objects.create(
            user=request.user,
            event_type=event.title,
            event_sub_type=event_sub_type,
            date=date,
            venue=venue,
            additional_details=additional_details
        )
        messages.success(request, f'Successfully booked {event.title}!')
        return redirect('home')
    
    return render(request, 'events/booking_form.html', {'event': event})

def our_team(request):
    return render(request, 'events/our_team.html')

def our_story(request):
    return render(request, 'events/our_story.html')

def contact(request):
    if request.method == 'POST':
        messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
        return redirect('contact')
    return render(request, 'events/contact.html')

def enquiry(request):
    if request.method == 'POST':
        messages.success(request, 'Your enquiry has been submitted successfully!')
        return redirect('enquiry')
    return render(request, 'events/enquiry.html')
