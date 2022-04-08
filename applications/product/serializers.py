from rest_framework import serializers

from applications.product.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'owner', 'name', 'description', 'price', 'category', 'images') # images = related name в модельках




