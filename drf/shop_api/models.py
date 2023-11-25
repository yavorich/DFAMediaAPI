from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .enums import StatusEnum, RoleEnum
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        '''Create and save a user with the given email, and
        password.
        '''
        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must have is_staff=True.'
            )
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must have is_superuser=True.'
            )

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    password = models.CharField(_("Пароль"), max_length=128)
    last_login = models.DateTimeField(
        _("Последний вход"), blank=True, null=True
    )
    email = models.EmailField(
        unique=True,
        max_length=255,
        blank=False,
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    first_name = models.CharField(
        _('Имя'),
        max_length=31,
        blank=True,
        null=True,
    )
    last_name = models.CharField(
        _('Фамилия'),
        max_length=31,
        blank=True,
        null=True,
    )
    avatar = models.URLField(_("Аватар"), blank=True, null=True)
    role = models.CharField(
        _("Роль"),
        max_length=255,
        choices=RoleEnum.choices(),
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Category(models.Model):
    title = models.CharField(_("Название"), max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent_category = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children",
    )

    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):
    title = models.CharField(_("Название"), max_length=100)
    description = models.CharField(max_length=250)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    in_stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name="products",
    )


class Order(models.Model):
    status = models.CharField(
        _("Статус"), max_length=255,
        choices=StatusEnum.choices(),
        default=StatusEnum.WAITING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="orders"
    )


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name="items", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, related_name="order_items", on_delete=models.CASCADE
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    quantity = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        self.price = self.product.price
        super().save(*args, **kwargs)


class ProductWaitList(models.Model):
    product = models.ForeignKey(
        Product, related_name="waits", on_delete=models.CASCADE
    )
    customer = models.ForeignKey(
        User, related_name="waits", on_delete=models.CASCADE
    )
    quantity_need = models.PositiveIntegerField()
