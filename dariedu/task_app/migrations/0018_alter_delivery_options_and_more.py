# Generated by Django 5.1 on 2024-09-11 12:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task_app', '0017_merge_20240911_1540'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='delivery',
            options={},
        ),
        migrations.AlterModelOptions(
            name='deliveryassignment',
            options={'verbose_name': 'доставка волонтера', 'verbose_name_plural': 'доставки волонтеров'},
        ),
    ]
