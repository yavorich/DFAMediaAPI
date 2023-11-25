from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product, ProductWaitList
from .utils import create_waitlist_email


@receiver(post_save, sender=Product)
def notify_waitlist_subscribers(sender, instance: Product, **kwargs):
    waitlist_subscribers = ProductWaitList.objects.filter(product=instance)
    for subscriber in waitlist_subscribers:
        if subscriber.quantity_need <= instance.in_stock:
            email = create_waitlist_email(instance, subscriber)
            with open("shop_api/logs/notifications.txt", "a") as f:
                f.write(email)

            subscriber.delete()  # можно не удалять, а добавить статус "sent"
