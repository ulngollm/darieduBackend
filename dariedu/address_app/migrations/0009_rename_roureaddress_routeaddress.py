# Generated by Django 5.1 on 2024-09-02 09:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('address_app', '0008_alter_routesheet_map'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RoureAddress',
            new_name='RouteAddress',
        ),
    ]