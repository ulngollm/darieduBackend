# Generated by Django 5.1 on 2024-08-26 18:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0003_alter_user_city_alter_user_email_alter_user_is_staff_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rating',
            options={'verbose_name': 'рейтинг', 'verbose_name_plural': 'рейтинги'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'пользователь', 'verbose_name_plural': 'пользователи'},
        ),
    ]
