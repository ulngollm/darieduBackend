# Generated by Django 5.1 on 2024-11-07 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statistics_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='volunteerstats',
            name='week',
            field=models.PositiveIntegerField(verbose_name='Неделя'),
        ),
    ]
