# Generated by Django 5.1 on 2024-10-14 01:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback_app', '0006_alter_feedback_text_alter_photoreport_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='requestmessage',
            name='type',
            field=models.CharField(default='стать куратором', max_length=255, verbose_name='тип'),
        ),
    ]