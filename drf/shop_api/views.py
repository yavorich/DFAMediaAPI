from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .permissions import IsRepresentOrReadOnly
from . import serializers
from .models import User, Category, Product, Order, ProductWaitList
from .filters import ProductFilter
from .tasks import send_notification


class UserListView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer


class CategoryListView(generics.ListCreateAPIView):
    permission_classes = [IsRepresentOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsRepresentOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


class ProductListView(generics.ListCreateAPIView):
    permission_classes = [IsRepresentOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
    filterset_class = ProductFilter


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsRepresentOrReadOnly]
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer


class OrderListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = serializers.OrderSerializer


class OptOrderListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
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
                product_id,
                list(subscribers.values_list('id', flat=True))
            )
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_204_NO_CONTENT)
