from .models import ProductWaitList, Product, SpecialOffer, User
from datetime import datetime


def create_waitlist_email(product: Product,
                          subscriber: ProductWaitList) -> str:
    product_name = product.title
    customer_email = subscriber.customer.email
    subject = f"Товар {product_name} теперь в наличии!"
    message = (
        "Добрый день! Недавно вы интересовались товаром "
        + f"{product_name}. Этот товар теперь в наличии. "
        + "Если вам подходит этот вариант - "
        + "пожалуйста, свяжитесь с нами."
    )
    email = (f"To: {customer_email}\n"
             + f"Subject: {subject}\n\n"
             + f"Message: {message}\n\n")
    return email


def create_special_offer_email(offer: SpecialOffer, user: User):
    subject = "Новое специальное предложение для Вас!"
    message = (
        f'Добрый день! У нас проходит акция "{offer.title}"!\n'
        + f'{offer.description}\n\n'
        + "Спешите воспользоваться уникальным предложением до "
        + f"{datetime.strftime(offer.end_date, '%d.%m.%Y')}!"
    )
    email = (f"To: {user.email}\n"
             + f"Subject: {subject}\n\n"
             + f"Message: {message}\n\n")
    return email
