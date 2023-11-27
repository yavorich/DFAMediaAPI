from celery import shared_task
from .utils import create_waitlist_email, create_special_offer_email
from .models import Product, ProductWaitList, SpecialOffer, User
from .enums import RoleEnum


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


@shared_task
def send_special_offer():
    try:
        offer = SpecialOffer.objects.first()
    except SpecialOffer.DoesNotExist:
        return
    users = User.objects.filter(is_active=True, role=RoleEnum.CLIENT)
    if not users or not offer:
        return
    result = ""
    for user in users:
        result += create_special_offer_email(offer, user)
    with open("shop_api/logs/offers.txt", "a") as f:
        f.write(result)
