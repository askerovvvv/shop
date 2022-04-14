from django.contrib import admin

from applications.product.models import *

admin.site.register(Category)
# admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Rating)

class ImageInAdmin(admin.TabularInline):
    model = Image
    fields = ('image', )
    max_num = 5                                 # Написали эти классы чтобы в админке в Products можно было добавить также и фотографию
                                                #
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ImageInAdmin
    ]
