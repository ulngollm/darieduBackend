# Generated by Django 5.1 on 2024-11-10 20:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address_app', '0021_beneficiar_photo_link'),
        ('task_app', '0027_alter_deliveryassignment_options_remove_task_price_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='routesheet',
            name='user',
        ),
        migrations.CreateModel(
            name='RouteAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='route_assignments', to='task_app.delivery', verbose_name='доставка')),
                ('route_sheet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='address_app.routesheet', verbose_name='маршрутный лист')),
                ('volunteer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='route_assignments', to=settings.AUTH_USER_MODEL, verbose_name='волонтёр')),
            ],
            options={
                'verbose_name': 'маршрутный лист волонтёра',
                'verbose_name_plural': 'маршрутные листы волонтёров',
            },
        ),
    ]