from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.views import View
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import *
from rest_framework.mixins import * #ListModelMixin, CreateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ViewSet

from applications.product.filters import ProductFilter
from applications.product.models import Product, Rating, Category
from applications.product.permissions import IsAdmin
from applications.product.serializers import ProductSerializer, RatingSerializers, CategorySerializers


class LargeResultsSetPagination(PageNumberPagination):      # РЕКОМЕНДУЕТСЯ так называть класс если хотим переопределить пагинацию
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 100


# class ListCreateView(ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]  # указали что будем работать с фильтрацией
#     filterset_fields = ['category', 'owner']    # указали какие поля будем фильтровать
#     # search_fields = ['name', 'description', ] # поиск по
#     # filterset_class = ProductFilter # импорт из filters.py
#     ordering_fields = ['id'] # группировка с id
#
#     def get_queryset(self):  # Поисковик без наших библеотек
#         queryset = super().get_queryset()
#         search = self.request.query_params.get('search') # это то что стоит после ? знака в поисковике
#         print(search)
#         # queryset111 = None
#         if search:
#             queryset = queryset.filter(Q(name__icontains=search) | Q(description__icontains=search)) #
#         return queryset
#     # permission_classes = [IsAuthenticatedOrReadOnly] # для регистрированных пользователей список товаров #IsAdminUser
#     # pagination_class = None # для этой вьюшки выключили глобальную пагинацию
#     # pagination_class = LargeResultsSetPagination
#
#
# class DeleteUpdateRetriveView(RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = [IsAdmin]


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = LargeResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]  # локально указали чот будет фильтрация, поиск, ordering - группировка
    # filterset_fields = ['category', 'owner']    # указали по каким поля будем фильтровать
    filterset_class = ProductFilter     #  свой кастомный класс сделали
    ordering_fields = ['id', 'price']
    search_fields = ['name', 'description']

    def get_permissions(self):
        print(self.action) # action прилетает запрос GET POST
        if self.action in ['list', 'retrieve']: # GET в APIView list
            permissions = [] # всем доступно
        elif self.action == 'rating':
            permissions = [IsAuthenticated]
        else:
            permissions = [IsAuthenticated] # если POST,Delete и т.д запрос зарегистрируйся
        return [permission() for permission in permissions]

    def perform_create(self, serializer):

        serializer.save(owner=self.request.user)   # при создании продукта нам не придется ввести кто owner так как будет автоматически залогинненого пользователя
        # переходим в serializers и настраиваем

    @action(methods=['POST'], detail=True) # detail=True
    def rating(self, request, pk): # pk - к определонному товару     # http://localhost:8000/product/id_product/rating/
        serializer = RatingSerializers(data=request.data) # хранятся данные которые мы вели в теле запроса
        serializer.is_valid(raise_exception=True)

        try: # проверяем есть ли такой пользователь с таким продуктом и user
            obj = Rating.objects.get(product=self.get_object(), owner=request.user) # product=self.get_object() - тот продукт с которым мы хотим работать
            obj.rating = request.data['rating'] # если есть такой рейтинг обнови его
        except Rating.DoesNotExist:
            obj = Rating(owner=request.user, product=self.get_object(), rating=request.data['rating']) # если не найдет создаст новый рейтинг

        obj.save()
        return Response(request.data, status=status.HTTP_201_CREATED)


class CategoryListCreateView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [IsAuthenticated]


class CategoryRetriveDeleteUpdateView(RetrieveUpdateDestroyAPIView):
    lookup_field = 'slug'  # (за каким полем следить)
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
    permission_classes = [IsAuthenticated]


# class ProductViewSet(ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin, GenericViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

#
# class ProductViewSet(ViewSet):
#     def list(self, request):
#         pass
#     def create(self):
#         pass
#     def retrieve(self):
#         pass
#     def update(self):
#         pass
#     def destroy(self):
#         pass
