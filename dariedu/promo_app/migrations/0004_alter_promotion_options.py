# Generated by Django 5.1 on 2024-08-26 18:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('promo_app', '0003_alter_promotion_category_alter_promotion_city_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='promotion',
            options={'verbose_name': 'акция', 'verbose_name_plural': 'акции'},
        ),
    ]