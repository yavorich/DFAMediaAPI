from django.urls import path
from . import views

urlpatterns = [
    path("users/", views.UserListView.as_view(), name="user-list"),
    path("users/<int:pk>/", views.UserDetailView.as_view(), name="user-detail"),
    path("category/", views.CategoryListView.as_view(), name="category-list"),
    path("category/<int:pk>/", views.CategoryDetailView.as_view(), name="category-detail"),
    path("orders/", views.OrderListView.as_view(), name="order-list"),
    path("orders/<int:pk>/", views.OrderDetailView.as_view(), name="order-detail"),
    path("products/", views.ProductListView.as_view(), name="product-list"),
    path("products/<int:pk>/", views.ProductDetailView.as_view(), name="product-detail"),
    path("opt-orders/", views.OptOrderListView.as_view(), name="opt-order"),
    path("notification/", views.NotificationCreateView.as_view(), name="notification"),
    path("special-offer/", views.SpecialOfferListView.as_view(), name="special-offer"),
]
