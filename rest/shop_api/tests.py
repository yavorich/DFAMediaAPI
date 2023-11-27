from rest_framework.test import APITestCase, APIClient
from django.test import TestCase, TransactionTestCase
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from celery.contrib.testing.worker import start_worker
from rest_framework import status
from rest.celery import app
from .models import Product, User, ProductWaitList
from .models import Order, OrderItem
from .enums import RoleEnum, StatusEnum
from .utils import create_waitlist_email
from decimal import Decimal
import os


class OrdersTestCase(APITestCase):
    def setUp(self) -> None:
        User.objects.create(
            email="test@example.com",
            password=make_password('123'),
            role=RoleEnum.CLIENT
        )
        Product.objects.create(
            title="test_title",
            description="test_description",
            price=999.99,
            in_stock=10,
        )
        self.client = APIClient()
        self.client.login(email="test@example.com", password='123')

    def test_create_order(self):
        # создание тестовых данных
        product = Product.objects.last()
        user = User.objects.last()

        # отправка post-запроса
        url = reverse("opt-order")
        data = {"items": [{"product": product.pk, "quantity": 10}],
                "customer": user.pk}
        response = self.client.post(url, data, format="json")

        # проверка статус-кода
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # проверка создания ордера и его элемента
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)

        # проверка полей ордера
        order = Order.objects.get(pk=1)
        self.assertEqual(order.customer.pk, user.pk)
        self.assertEqual(order.status, StatusEnum.WAITING)

        # проверка полей элемента ордера
        order_item = OrderItem.objects.get(pk=1)
        self.assertEqual(order_item.product.pk, product.pk)
        self.assertEqual(order_item.order.pk, order.pk)
        self.assertEqual(order_item.quantity, 10)
        self.assertEqual(order_item.price, product.price)

        # проверка фиксации цены в ордер-айтеме
        product.price = Decimal(111.11)
        product.save()
        self.assertNotEqual(order_item.price, product.price)

    def test_create_over_quantity_order(self):
        """
        Тестирование попытки выставления ордера с кол-вом товара,
        превышающим кол-во товара на складе.
        """
        product = Product.objects.last()
        product.in_stock = 1  # продукт есть, но его мало
        product.save()

        user = User.objects.last()

        # отправка post-запроса
        url = reverse("opt-order")
        data = {"items": [{"product": product.pk, "quantity": 20}],
                "customer": user.pk}
        response = self.client.post(url, data, format="json")

        # проверка статус-кода
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # при наличии товара в недостаточном количестве,
        # ордеров и записи в wait-list быть не должно
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(OrderItem.objects.count(), 0)
        self.assertEqual(ProductWaitList.objects.count(), 0)

        # отправка ордера на отсутствующий продукт
        product.in_stock = 0
        product.save()
        response = self.client.post(url, data, format="json")

        # проверка статус-кода
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # проверка отсутствия ордеров и наличия записи в wait-list
        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(OrderItem.objects.count(), 0)
        self.assertEqual(ProductWaitList.objects.count(), 1)

        # проверка полей записи
        subscriber = ProductWaitList.objects.last()
        self.assertEqual(subscriber.customer.pk, user.pk)
        self.assertEqual(subscriber.product.pk, product.pk)


class NotificationsTestCase(TransactionTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.celery_worker = start_worker(app, perform_ping_check=False)
        cls.celery_worker.__enter__()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.celery_worker.__exit__(None, None, None)

    def setUp(self) -> None:
        user = User.objects.create(
            email="test@example.com",
            password=make_password('123'),
            role=RoleEnum.REPRESENT
        )
        product = Product.objects.create(
            title="test_title",
            description="test_description",
            price=999.99,
            in_stock=0,
        )
        ProductWaitList.objects.create(
            customer=user, product=product
        )
        self.client = APIClient()
        self.client.login(email="test@example.com", password='123')

    def test_send_waitlist_notification(self):

        # создание тестовых объектов
        product = Product.objects.last()
        subscriber = ProductWaitList.objects.last()

        # отправка post-запроса
        save_path = "shop_api/logs/notifications.txt"
        if os.path.exists(save_path):
            os.remove(save_path)
        url = reverse("notification")
        data = {"product": product.id}
        response = self.client.post(url, data, format="json")

        # проверка статус-кода
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # рассылка не должна произойти, если товар не в наличии
        self.assertEqual(os.path.exists(save_path), False)

        # запрос с товаром в наличии
        product.in_stock = 1
        product.save()
        response = self.client.post(url, data, format="json")

        # проверка статус-кода
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # запись должна быть удалена
        self.assertEqual(ProductWaitList.objects.count(), 0)
        # рассылка должна была произойти
        self.assertEqual(os.path.exists(save_path), True)
        # проверка корректности сообщения
        email = create_waitlist_email(product, subscriber)
        try:
            with open("shop_api/logs/notifications.txt", "r") as f:
                content = f.read()
                self.assertEqual(content, email)
        except FileNotFoundError:
            pass
