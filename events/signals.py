from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Booking

@receiver(pre_save, sender=Booking)
def notify_status_change(sender, instance, **kwargs):
    if instance.id:
        try:
            previous_booking = Booking.objects.get(id=instance.id)
            if previous_booking.status != instance.status:
                subject = f'Booking Status Updated: {instance.event_type}'
                message = f'Hi {instance.user.username},\n\n' \
                          f'The status of your booking for "{instance.event_type}" on {instance.date} ' \
                          f'has been changed to: {instance.get_status_display()}.\n\n' \
                          f'Thank you,\nTriAura Events Team'
                recipient_list = [instance.user.email]
                if instance.user.email:
                    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list, fail_silently=True)
        except Booking.DoesNotExist:
            pass
