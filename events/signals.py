from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Booking

@receiver(pre_save, sender=Booking)
def notify_status_change(sender, instance, **kwargs):
    print(f"DEBUG: Signal triggered for booking ID: {instance.id}")
    if instance.id:
        try:
            previous_booking = Booking.objects.get(id=instance.id)
            print(f"DEBUG: Previous status: {previous_booking.status}, New status: {instance.status}")
            if previous_booking.status != instance.status:
                subject = f'Booking Status Updated: {instance.event_type}'
                message = f'Hi {instance.user.username},\n\n' \
                          f'The status of your booking for "{instance.event_type}" on {instance.date} ' \
                          f'has been changed to: {instance.get_status_display()}.\n\n' \
                          f'Thank you,\nTriAura Events Team'
                
                recipient_list = [instance.user.email]
                print(f"DEBUG: Attempting to send email to {recipient_list}")
                
                if instance.user.email:
                    send_mail(
                        subject, 
                        message, 
                        settings.DEFAULT_FROM_EMAIL, 
                        recipient_list, 
                        fail_silently=False
                    )
                    print("DEBUG: Email sent successfully.")
                else:
                    print("DEBUG: User has no email address.")
            else:
                print("DEBUG: Status did not change.")
        except Booking.DoesNotExist:
            print("DEBUG: Booking does not exist in DB yet.")
        except Exception as e:
            print(f"DEBUG: Error in notify_status_change: {str(e)}")
