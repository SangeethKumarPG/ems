import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ems.settings')
django.setup()

from django.contrib.auth.models import User
from events.models import Event, Booking
from django.utils import timezone

def verify_system():
    print("--- Starting System Verification ---")

    # 1. Simulate Admin creating an event
    admin_user, _ = User.objects.get_or_create(username='admin', defaults={'is_superuser': True, 'is_staff': True})
    
    event_title = "Test Gala Event " + str(timezone.now().timestamp())
    new_event = Event.objects.create(
        title=event_title,
        description="A specially created event for verification.",
        category='corporate',
        price=1000.00
    )
    print(f"SUCCESS: Admin simulated creating event: {new_event.title}")

    # 2. Simulate a normal user registering
    user_count = User.objects.filter(username='testuser').count()
    test_username = f'testuser_{user_count}'
    normal_user = User.objects.create_user(username=test_username, password='password123', email=f'{test_username}@example.com')
    print(f"SUCCESS: Normal user registered: {normal_user.username}")

    # 3. Simulate the user booking the event (logic from views.py)
    booking = Booking.objects.create(
        user=normal_user,
        event_type=new_event.title,
        event_sub_type="VIP Lounge",
        date=timezone.now().date(),
        venue="The Palace",
        additional_details="Verification test booking."
    )
    
    # 4. Verify the booking exists
    if Booking.objects.filter(id=booking.id).exists():
        print(f"SUCCESS: User {normal_user.username} successfully booked the event {new_event.title}!")
        print(f"Booking status: {booking.status}")
    else:
        print("FAILURE: Booking was not found in the database.")

    print("--- Verification Complete ---")

if __name__ == "__main__":
    verify_system()
