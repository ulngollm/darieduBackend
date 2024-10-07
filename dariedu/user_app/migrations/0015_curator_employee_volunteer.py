# Generated by Django 5.1 on 2024-10-06 12:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0014_user_metier'),
    ]

    operations = [
        migrations.CreateModel(
            name='Curator',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('user_app.user',),
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('user_app.user',),
        ),
        migrations.CreateModel(
            name='Volunteer',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('user_app.user',),
        ),
    ]
