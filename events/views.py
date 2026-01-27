from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Event, Booking
from .forms import BookingForm, ContactForm, EnquiryForm
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
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.event_type = event.title
            booking.save()
            messages.success(request, f'Successfully booked {event.title}!')
            return redirect('home')
    else:
        form = BookingForm()
    
    return render(request, 'events/booking_form.html', {'event': event, 'form': form})

def our_team(request):
    return render(request, 'events/our_team.html')

def our_story(request):
    return render(request, 'events/our_story.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the data in form.cleaned_data
            messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'events/contact.html', {'form': form})

def enquiry(request):
    if request.method == 'POST':
        form = EnquiryForm(request.POST)
        if form.is_valid():
            # Process the data (e.g., send email or save to DB)
            messages.success(request, 'Your enquiry has been submitted successfully!')
            return redirect('enquiry')
    else:
        form = EnquiryForm()
    return render(request, 'events/enquiry.html', {'form': form})
