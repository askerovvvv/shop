from django.db.models import Q
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

from applications.product.filters import ProductFilter
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
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]  # указали что будем работать с фильтрацией
    filterset_fields = ['category', 'owner']    # указали какие поля будем фильтровать
    # search_fields = ['name', 'description', ] # поиск по
    # filterset_class = ProductFilter # импорт из filters.py
    ordering_fields = ['id'] # группировка с id

    def get_queryset(self):  # Поисковик без наших библеотек
        queryset = super().get_queryset()
        search = self.request.query_params.get('search') # это то что стоит после ? знака в поисковике
        print(search)
        # queryset111 = None
        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(description__icontains=search)) #
        return queryset
    # permission_classes = [IsAuthenticatedOrReadOnly] # для регистрированных пользователей список товаров #IsAdminUser
    # pagination_class = None # для этой вьюшки выключили глобальную пагинацию
    # pagination_class = LargeResultsSetPagination


class DeleteUpdateRetriveView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdmin]







