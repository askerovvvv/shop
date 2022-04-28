# Generated by Django 4.0.3 on 2022-04-22 14:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0004_rating'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField(default=False, verbose_name='ЛААААААААЙК')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like', to=settings.AUTH_USER_MODEL, verbose_name='Владелец лайка')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='like', to='product.product', verbose_name='Продукт')),
            ],
        ),
    ]
