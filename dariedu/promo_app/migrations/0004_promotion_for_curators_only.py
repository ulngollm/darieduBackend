# Generated by Django 5.1 on 2024-08-23 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('promo_app', '0003_alter_promotion_category_alter_promotion_city_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='promotion',
            name='for_curators_only',
            field=models.BooleanField(default=False, verbose_name='только для кураторов'),
        ),
    ]
