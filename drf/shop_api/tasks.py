from celery import shared_task
from .utils import create_waitlist_email
from .models import Product, ProductWaitList


@shared_task
def send_notification(product_id, subscribers_ids):
    product = Product.objects.get(id=product_id)
    if product.in_stock < 1:
        return
    subscribers = ProductWaitList.objects.filter(
        id__in=subscribers_ids
    )
    for subscriber in subscribers:
        email = create_waitlist_email(product, subscriber)
        with open("shop_api/logs/notifications.txt", "a") as f:
            f.write(email)

        subscriber.delete()  # можно не удалять, а добавить статус "sent"
