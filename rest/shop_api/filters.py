from django_filters import rest_framework as filters
from .models import Product


class ProductFilter(filters.FilterSet):
    in_stock = filters.BooleanFilter(method="filter_in_stock")
    price = filters.NumberFilter(field_name="price")
    created_at = filters.DateFilter(method="filter_created_at")
    category_id = filters.NumberFilter(field_name="category")

    def filter_in_stock(self, queryset, name, value):
        if value:
            # Фильтрация по наличию товара
            queryset = queryset.filter(in_stock__gt=0)
        else:
            # Фильтрация по отсутствию товара
            queryset = queryset.filter(in_stock=0)
        return queryset

    def filter_created_at(self, queryset, name, value):
        # перевод из datetime в date
        return queryset.filter(**{"created_at__date": value})

    class Meta:
        model = Product
        fields = ["in_stock", "price", "created_at", "category_id"]
