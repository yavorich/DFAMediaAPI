from rest_framework import serializers
from .models import Category, Product, Order, \
    User, OrderItem, ProductWaitList


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at", "products")


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ("product", "price", "quantity")
        read_only_fields = ("price", )


class OptOrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ("items", "customer", "status", "created_at", "updated_at")
        read_only_fields = ("created_at", "updated_at")

    @staticmethod
    def is_sufficient_quantity_available(validated_data):
        items_data = validated_data["items"]
        valid = True
        for item_data in items_data:
            product = item_data["product"]
            quantity = item_data["quantity"]
            if quantity > product.in_stock:
                valid = False
                ProductWaitList.objects.create(
                    product=product,
                    customer=validated_data["customer"],
                    quantity_need=quantity
                )
        return valid

    def create(self, validated_data):
        if not self.is_sufficient_quantity_available(validated_data):
            raise serializers.ValidationError(
                "Некоторых товаров не хватает"
            )

        items_data = validated_data.pop("items")
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            product = item_data["product"]
            quantity = item_data["quantity"]
            OrderItem.objects.create(
                order=order, product=product, quantity=quantity
            )
        return order
