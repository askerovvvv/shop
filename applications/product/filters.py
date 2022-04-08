from django_filters import rest_framework as filters

from applications.product.models import Product


class ProductFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains') # icontains = не смотря на регистр
    price_from = filters.NumberFilter(field_name='price', lookup_expr='gte') # gte = больше или равно, lookup_expr = параметр того как  фильтровать
    price_to = filters.NumberFilter(field_name='price', lookup_expr='lte') ###### field_name = !?

    class Meta:
        model = Product
        fields = ['category', 'price'] ## по умолчанию по каким полям



