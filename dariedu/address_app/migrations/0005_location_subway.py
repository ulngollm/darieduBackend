# Generated by Django 5.1 on 2024-08-23 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address_app', '0004_alter_address_address_alter_address_link_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='subway',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='метро'),
        ),
    ]
