from django.db import models

from user_app.models import User
from address_app.models import RouteSheet, City


class Delivery(models.Model):
    date = models.DateTimeField(verbose_name='дата доставки')
    price = models.PositiveIntegerField('часы')
    is_free = models.BooleanField(default=True, verbose_name='свободная')
    is_active = models.BooleanField(default=True, verbose_name='активная')

    volunteer = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='волонтер')
    route_sheet = models.ForeignKey(RouteSheet, on_delete=models.CASCADE, related_name='delivery', verbose_name='маршрутный лист') # TODO: add null=True??


class Task(models.Model):
    category = models.CharField(max_length=255, verbose_name='категория')
    name = models.CharField(max_length=255, verbose_name='название')
    price = models.PositiveIntegerField(verbose_name='часы')
    description = models.TextField(blank=True, null=True, verbose_name='описание')
    date = models.DateTimeField(verbose_name='дата')
    duration = models.PositiveIntegerField(verbose_name='длительность')
    quantity = models.PositiveIntegerField(verbose_name='количество волонтеров')
    is_active = models.BooleanField(default=True, verbose_name='активная')

    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True, verbose_name='город')
    curator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_curator', verbose_name='куратор')
    volunteer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='task_volunteer',
                                  verbose_name='волонтер')

    def __str__(self):
        return f'{self.name}, {self.date}'
