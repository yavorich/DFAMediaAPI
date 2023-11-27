from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from . import serializers
from .models import User, Category, Product, \
    Order, ProductWaitList, SpecialOffer
from .filters import ProductFilter
from .tasks import send_notification


class UserListView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class CategoryListView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


class ProductListView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    filterset_class = ProductFilter


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer


class OrderListView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer


class OptOrderListView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Order.objects.all()
    serializer_class = serializers.OptOrderSerializer


class NotificationCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        product_id = request.data["product"]
        product = Product.objects.get(id=product_id)
        if product.in_stock > 0:
            subscribers = ProductWaitList.objects.filter(product=product_id)
            send_notification.delay(
                product_id, list(subscribers.values_list("id", flat=True))
            )
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SpecialOfferListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        try:
            special_offer = SpecialOffer.objects.first()
        except SpecialOffer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.SpecialOfferSerializer(special_offer)
        return Response(serializer.data)

    def patch(self, request, format=None):
        try:
            special_offer = SpecialOffer.objects.first()
        except SpecialOffer.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.SpecialOfferSerializer(
            special_offer, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
