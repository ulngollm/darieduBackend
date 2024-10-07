# Generated by Django 5.1 on 2024-10-05 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0013_alter_user_consent_to_personal_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='metier',
            field=models.CharField(blank=True, choices=[('schoolchild', 'Школьник'), ('student', 'Студент'), ('work_on_himself', 'Работаю на себя'), ('work_for_hire', 'Работаю по найму'), ('pensioner', 'Пенсионер'), ('other', 'Другое')], default=None, max_length=50, null=True, verbose_name='род деятельности'),
        ),
    ]
