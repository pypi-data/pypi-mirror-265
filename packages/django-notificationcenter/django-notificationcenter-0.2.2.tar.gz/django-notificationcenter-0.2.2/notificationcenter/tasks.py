from .models import (
    Notification,
    NotificationTypeChoices,
    default_center as notification_center,
    notification_event,
)

def send_notification(notification_id):
    try:
        notification = Notification.objects.get(pk=notification_id)
    except Notification.DoesNotExist:
        # log(f'Notification not found (ID: {notification_id}', level=logging.ERROR)
        return True

    subscribers = notification_center.subscribers(notification.name, sender=notification.sender)
    if subscribers:
        notification_classes = notification_center.notification_classes(notification.name, sender=notification.sender)
        email_class = notification_classes.get(NotificationTypeChoices.EMAIL)
        if email_class:
            bcc = set([notification_center.email_accessor(user) for user in subscribers])
            bcc.discard(None)
            email = email_class(notification, bcc=bcc)
            email.send()

        sms_class = notification_classes.get(NotificationTypeChoices.SMS)
        if sms_class:
            recipients = set([notification_center.phone_accessor(user) for user in subscribers])
            recipients.discard(None)
            sms = sms_class(notification, recipients=recipients)
            sms.send()

    notification.mark_as_sent()
    return True
