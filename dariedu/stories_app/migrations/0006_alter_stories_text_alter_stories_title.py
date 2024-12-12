# Generated by Django 5.1 on 2024-12-01 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stories_app', '0005_remove_stories_link_name_remove_stories_media_files_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stories',
            name='text',
            field=models.TextField(default='some text', verbose_name='текст'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='stories',
            name='title',
            field=models.CharField(default=11, max_length=255, verbose_name='заголовок'),
            preserve_default=False,
        ),
    ]