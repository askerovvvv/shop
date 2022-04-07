from django.shortcuts import render
from rest_framework.generics import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from applications.product.models import Product
from applications.product.permissions import IsAdmin
from applications.product.serializers import ProductSerializer


class LargeResultsSetPagination(PageNumberPagination):      # РЕКОМЕНДУЕТСЯ так называть класс если хотим переопределить пагинацию
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100


class ListCreateView(ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly] # для регистрированных пользователей список товаров #IsAdminUser
    # pagination_class = None # для этой вьюшки выключили глобальную пагинацию
    # pagination_class = LargeResultsSetPagination


class DeleteUpdateRetriveView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdmin]







