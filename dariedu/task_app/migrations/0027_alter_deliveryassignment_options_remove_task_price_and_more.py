# Generated by Django 5.1 on 2024-10-14 01:22

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_app', '0026_alter_task_options_alter_taskcategory_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deliveryassignment',
            options={'verbose_name': 'доставка волонтёра', 'verbose_name_plural': 'доставки волонтёров'},
        ),
        migrations.RemoveField(
            model_name='task',
            name='price',
        ),
        migrations.AddField(
            model_name='task',
            name='curator_price',
            field=models.PositiveIntegerField(default=2, verbose_name='кураторские часы'),
        ),
        migrations.AddField(
            model_name='task',
            name='volunteer_price',
            field=models.PositiveIntegerField(default=2, verbose_name='волонтёрские часы'),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='volunteers_needed',
            field=models.PositiveIntegerField(default=1, verbose_name='требуется волонтёров'),
        ),
        migrations.AlterField(
            model_name='delivery',
            name='volunteers_taken',
            field=models.PositiveIntegerField(default=0, verbose_name='волонтёров взяли'),
        ),
        migrations.AlterField(
            model_name='deliveryassignment',
            name='volunteer',
            field=models.ManyToManyField(related_name='assignments', to=settings.AUTH_USER_MODEL, verbose_name='волонтёр'),
        ),
        migrations.AlterField(
            model_name='task',
            name='volunteers',
            field=models.ManyToManyField(blank=True, related_name='tasks', to=settings.AUTH_USER_MODEL, verbose_name='волонтёры'),
        ),
        migrations.AlterField(
            model_name='task',
            name='volunteers_needed',
            field=models.PositiveIntegerField(default=1, verbose_name='требуется волонтёров'),
        ),
        migrations.AlterField(
            model_name='task',
            name='volunteers_taken',
            field=models.PositiveIntegerField(default=0, verbose_name='волонтёров взяли'),
        ),
    ]