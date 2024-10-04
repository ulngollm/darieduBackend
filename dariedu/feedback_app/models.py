from django.db import models
from user_app.models import User
from promo_app.models import Promotion
from task_app.models import Delivery
from django.core.exceptions import ValidationError



class RequestMessage(models.Model):
    type = models.CharField(max_length=255, verbose_name='тип заявки')
    text = models.TextField(verbose_name='текст', blank=True, null=True)
    form = models.URLField(max_length=500, blank=True, null=True, verbose_name='форма')
    date = models.DateField(verbose_name='дата', auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'заявка'
        verbose_name_plural = 'заявки'


class Feedback(models.Model):
    TYPE_CHOICES = [
        ('delivery', 'Доставка'),
        ('promotion', 'Поощрение'),
    ]

    id = models.AutoField(primary_key=True, verbose_name="ID")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Тип отзыва")
    text = models.TextField(verbose_name="Текст отзыва")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Доставка", related_name="feedbacks")
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Поощрение", related_name="feedbacks")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def clean(self):
        # Проверка, что отзыв может быть только о доставке или поощрении, но не о двух одновременно
        if self.type == 'delivery' and not self.delivery:
            raise ValidationError("Для отзыва о доставке необходимо указать доставку.")
        if self.type == 'promotion' and not self.promotion:
            raise ValidationError("Для отзыва о поощрении необходимо указать поощрение.")
        if self.delivery and self.promotion:
            raise ValidationError("Отзыв может быть связан только с одной моделью: либо доставка, либо поощрение.")

    def __str__(self):
        if self.type == 'delivery':
            return f"Отзыв о доставке {self.delivery} от {self.user.name} {self.user.last_name}"
        elif self.type == 'promotion':
            return f"Отзыв о поощрении {self.promotion} от {self.user.name} {self.user.last_name}"
        return f"Отзыв от {self.user.name} {self.user.last_name}"

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'


class PhotoReport(models.Model):
    address = models.ForeignKey('address_app.Address', on_delete=models.CASCADE, verbose_name='адрес')
    photo = models.URLField(max_length=500, verbose_name='фото', blank=True, null=True)
    date = models.DateField(verbose_name='дата', auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='пользователь')
    comment = models.TextField(verbose_name='комментарий', blank=True, null=True)
