from celery import shared_task
from .models import Notification

@shared_task
def send_notification(user_id, message):
    # Create a notification for the user
    notification = Notification.objects.create(user_id=user_id, message=message)
    return notification.id