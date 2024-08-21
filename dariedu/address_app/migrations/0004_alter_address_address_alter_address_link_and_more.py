# Generated by Django 5.1 on 2024-08-21 08:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address_app', '0003_alter_address_route_sheet'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address',
            field=models.CharField(max_length=255, verbose_name='адрес'),
        ),
        migrations.AlterField(
            model_name='address',
            name='link',
            field=models.URLField(max_length=500, verbose_name='ссылка'),
        ),
        migrations.AlterField(
            model_name='address',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='address_location', to='address_app.location', verbose_name='локация'),
        ),
        migrations.AlterField(
            model_name='address',
            name='route_sheet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='address_route_sheet', to='address_app.routesheet', verbose_name='маршрутный лист'),
        ),
        migrations.AlterField(
            model_name='beneficiar',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='beneficiar_address', to='address_app.address', verbose_name='адрес'),
        ),
        migrations.AlterField(
            model_name='beneficiar',
            name='comment',
            field=models.TextField(blank=True, null=True, verbose_name='комментарий'),
        ),
        migrations.AlterField(
            model_name='beneficiar',
            name='full_name',
            field=models.CharField(max_length=255, verbose_name='ФИО'),
        ),
        migrations.AlterField(
            model_name='beneficiar',
            name='phone',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='телефон'),
        ),
        migrations.AlterField(
            model_name='city',
            name='city',
            field=models.CharField(max_length=255, unique=True, verbose_name='город'),
        ),
        migrations.AlterField(
            model_name='location',
            name='address',
            field=models.CharField(max_length=500, verbose_name='адрес'),
        ),
        migrations.AlterField(
            model_name='location',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='address_app.city', verbose_name='город'),
        ),
        migrations.AlterField(
            model_name='location',
            name='curator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='куратор'),
        ),
        migrations.AlterField(
            model_name='location',
            name='link',
            field=models.URLField(max_length=500, verbose_name='ссылка'),
        ),
        migrations.AlterField(
            model_name='routesheet',
            name='map',
            field=models.URLField(max_length=500, verbose_name='карта'),
        ),
    ]
