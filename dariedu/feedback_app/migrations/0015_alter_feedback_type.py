# Generated by Django 5.1 on 2024-12-11 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback_app', '0014_photoreport_is_absent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='type',
            field=models.CharField(choices=[('completed_delivery', 'Завершенная доставка'), ('canceled_delivery', 'Отмененная доставка'), ('completed_promotion', 'Завершенное поощрение'), ('canceled_promotion', 'Отмененное поощрение'), ('completed_task_curator', 'Завершенное доброе дело -  куратор'), ('completed_delivery_curator', 'Завершенная доставка - куратор'), ('completed_task', 'Завершенное доброе дело'), ('canceled_task', 'Отмененное доброе дело'), ('suggestion', 'Вопросы и предложения'), ('support', 'Техническая поддержка')], max_length=30, verbose_name='Тип обратной связи'),
        ),
    ]