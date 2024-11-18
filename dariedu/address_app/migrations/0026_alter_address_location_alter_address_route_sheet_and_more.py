# Generated by Django 5.1 on 2024-11-17 21:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address_app', '0025_alter_beneficiar_address_alter_beneficiar_comment_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='address_location', to='address_app.location', verbose_name='локация'),
        ),
        migrations.AlterField(
            model_name='address',
            name='route_sheet',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='address', to='address_app.routesheet', verbose_name='маршрутный лист'),
        ),
        migrations.AlterField(
            model_name='beneficiar',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='beneficiar', to='address_app.address', verbose_name='адрес проживания'),
        ),
        migrations.AlterField(
            model_name='location',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='address_app.city', verbose_name='город'),
        ),
        migrations.AlterField(
            model_name='location',
            name='curator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='куратор'),
        ),
        migrations.AlterField(
            model_name='routesheet',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='route_sheets', to='address_app.location', verbose_name='локация'),
        ),
    ]
