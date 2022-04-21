from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

User = get_user_model()


class Category(models.Model):
    slug = models.SlugField(max_length=30, primary_key=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.slug} - {self.description} "


class Product(models.Model):
    owner = models.ForeignKey(User, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    # image = models.ImageField(upload_to='images', null=True, blank=True) # скачиваем библеотеку для работы с ним (requirements.txt pillow)
    # likes = models.ManyToManyField(User, blank=True, related_name='likes')


    def __str__(self):
        return f'{self.id}'

class Image(models.Model):
    image = models.ImageField(upload_to='images')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')


class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='rating') # у рейтинга должен быть продукт к которому он принадлежит
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rating') # у рейтинга должен быть пользователь к которому он принадлежит
    rating = models.SmallIntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(5),
    ]) # сам рейтинг оценка от 1 до 5




