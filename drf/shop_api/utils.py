from .models import ProductWaitList, Product


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
