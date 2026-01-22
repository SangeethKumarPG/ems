import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ems.settings')
django.setup()

from events.models import Event

events_to_create = [
    {
        'title': 'Grand Wedding Decor',
        'description': 'A beautiful grand wedding setup with premium flowers and lighting.',
        'category': 'wedding',
        'image_url': 'https://i.pinimg.com/1200x/7c/94/77/7c9477dc7b139d45868aa0a3dd74b65d.jpg',
        'features': 'Premium Lotus Theme\nLED Lighting\nGrand Entrance Decor\nStage Decoration',
        'price': 4999.99
    },
    {
        'title': 'Birthday Bash',
        'description': 'Exciting birthday party setup with balloons and theme-based decor.',
        'category': 'birthday',
        'image_url': 'https://i.pinimg.com/1200x/dd/a1/18/dda118788904d1ae1affe3ca186620ee.jpg',
        'features': 'Balloon Arches\nTheme Cutouts\nCake Table Decor\nKids Play Area Setup',
        'price': 1499.99
    },
    {
        'title': 'Corporate Excellence',
        'description': 'Professional and sleek corporate event management.',
        'category': 'corporate',
        'image_url': 'https://i.pinimg.com/736x/7a/da/fb/7adafbcc061836f2bfdf54a35be6745f.jpg',
        'features': 'Professional Stage\nAudio-Visual Setup\nNetworking Area Decor\nBranding Panels',
        'price': 2999.99
    }
]

for event_data in events_to_create:
    Event.objects.get_or_create(
        title=event_data['title'],
        defaults=event_data
    )

print("Events seeded successfully!")
