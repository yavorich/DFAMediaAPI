from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .permissions import IsRepresentOrReadOnly
from . import serializers
from .models import User, Category, Product, Order


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
