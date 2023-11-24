from django.urls import path
from . import views

urlpatterns = [
    path("users/", views.UserListView.as_view(), name="user_list"),
    path("users/<int:pk>/", views.UserDetailView.as_view(), name="user_detail"),
    path("category/", views.CategoryListView.as_view(), name="category_list"),
    path("category/<int:pk>/", views.CategoryDetailView.as_view(), name="category_detail"),
    path("orders/", views.OrderListView.as_view(), name="order_list"),
    path("orders/<int:pk>/", views.OrderDetailView.as_view(), name="order_detail"),
    path("products/", views.ProductListView.as_view(), name="product_list"),
    path("products/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("opt-orders/", views.OptOrderListView.as_view(), name="opt_order_list"),
]
