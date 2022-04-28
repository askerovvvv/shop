from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from applications.cart.models import Cart
from applications.cart.serializers import CartSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer # ... - NONE
    permission_classes = [IsAuthenticated]

    def get_queryset(self): # все что мы видим | переопределяем чтобы ограничить доступ
        user = self.request.user
        queryset = super().get_queryset()
        queryset = queryset.filter(user=user)      #### первый user откуда
        return queryset
