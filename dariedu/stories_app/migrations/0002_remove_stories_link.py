# Generated by Django 5.1 on 2024-09-11 09:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stories',
            name='link',
        ),
    ]