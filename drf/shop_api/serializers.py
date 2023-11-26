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
    def validate_sufficient_quantity(validated_data):
        '''
        Проверка на наличие нужного кол-ва каждого товара
        Если товара нет на складе, будет создана запись в wait-list
        '''
        items_data = validated_data["items"]
        valid = True
        for item_data in items_data:
            product = item_data["product"]
            quantity = item_data["quantity"]
            in_stock = product.in_stock
            if quantity > in_stock:
                valid = False
                if in_stock == 0:
                    ProductWaitList.objects.get_or_create(
                        product=product,
                        customer=validated_data["customer"],
                    )
        return valid

    def create(self, validated_data):
        # проверка на наличие товаров на складе
        if not self.validate_sufficient_quantity(validated_data):
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
