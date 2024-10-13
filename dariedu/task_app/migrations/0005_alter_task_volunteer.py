# Generated by Django 5.1 on 2024-08-21 08:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_app', '0004_alter_delivery_date_alter_task_date'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='volunteer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='task_volunteer', to=settings.AUTH_USER_MODEL, verbose_name='волонтёр'),
        ),
    ]
