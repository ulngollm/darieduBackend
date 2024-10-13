# Generated by Django 5.1 on 2024-09-04 15:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_app', '0007_merge_20240827_1622'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='delivery',
            options={},
        ),
        migrations.AddField(
            model_name='delivery',
            name='in_execution',
            field=models.BooleanField(default=False, verbose_name='выполняется'),
        ),
        migrations.AddField(
            model_name='delivery',
            name='is_completed',
            field=models.BooleanField(default=False, verbose_name='завершена'),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='volunteer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deliveries', to=settings.AUTH_USER_MODEL, verbose_name='волонтёр'),
        ),
    ]
