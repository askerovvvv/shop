from django.contrib.auth import get_user_model
from rest_framework import serializers

from applications.product.models import Product, Image, Rating, Category, Like


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def validate_title(self, title):
        if Category.objects.filter(slug=title.lower()).exists():
            raise serializers.ValidationError('Такое название уже существует')
        return title

    def to_representation(self, instance):
        representation = super().to_representation(instance)  # в данном коде он отрабатывает также как обычно и записывает данные в переменную
        if not instance.parent:
            representation.pop('parent')
        return representation


class ProductImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')    # это поле только для чтение(не обьязателньо заполнять)    || source='owner.email' = отображай email ownera
    images = ProductImageSerializers(many=True, read_only=True)      # чтобы обрабатывать несколько картин

    class Meta:
        model = Product
        fields = ('id', 'owner', 'name', 'description', 'price', 'category', 'images',) # images = related name в модельках

    def create(self, validated_data): # переопределяем create он работает последним
        request = self.context.get('request') # получили файлы которые передали в запросе
        images_data = request.FILES # занесли в переменное
        product = Product.objects.create(**validated_data) # validated_data хранятся те данные которые указали помимо images
        for image in images_data.getlist('images'): # вытащи поля images
            Image.objects.create(product=product, image=image) # models
        return product

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        rating_result = 0
        for i in instance.rating.all():
            rating_result += int(i.rating)
        print(instance.rating.all().count())
        if instance.rating.all().count() == 0:
            representation['rating'] = rating_result
        # representation['owner'] = 'f' переопределили представление пользователя
        else:
            representation['rating'] = rating_result / instance.rating.all().count()

        representation['like'] = instance.like.filter(like=True).count()   # записываем те лайки которые like=True

        return representation


class RatingSerializers(serializers.ModelSerializer):
    # owner = serializers.EmailField(required=False) # не обьязателньо к заполнению

    class Meta:
        model = Rating
        fields = ('rating', ) # 'owner'


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'




