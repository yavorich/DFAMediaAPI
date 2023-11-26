from django.contrib import admin
from .models import User, Category, Product, Order


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "first_name", "last_name", "role"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "parent_category"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["title", "description", "price", "in_stock", "category"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    exclude = ["created_at", "updated_at"]
