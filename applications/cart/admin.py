from django.contrib import admin

from applications.cart.models import Cart, CartItem

admin.site.register(Cart)
admin.site.register(CartItem)

