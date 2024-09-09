from django.db import models
from django.core.exceptions import ValidationError
from user_app.models import User

from address_app.models import RouteSheet, City
from user_app.models import User


class Delivery(models.Model):
    date = models.DateTimeField(verbose_name='дата доставки')
    price = models.PositiveIntegerField('часы')
    is_free = models.BooleanField(default=True, verbose_name='свободная')
    is_active = models.BooleanField(default=True, verbose_name='активная')
    is_completed = models.BooleanField(default=False, verbose_name='завершена')
    in_execution = models.BooleanField(default=False, verbose_name='выполняется')

    volunteer = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='deliveries',
                                  null=True, blank=True, verbose_name='волонтер')
    route_sheet = models.ForeignKey(RouteSheet, on_delete=models.CASCADE, related_name='delivery', verbose_name='маршрутный лист') # TODO: add null=True??

    def clean(self):
        if self.is_free:
            self.is_completed = False
            self.in_execution = False
            if self.volunteer:
                raise ValidationError({'volunteer': 'Volunteer should be False if delivery is free'})
        elif self.is_completed:
            self.is_active = False
            self.is_free = False
            self.in_execution = False
        elif self.in_execution:
            self.is_active = True
            self.is_free = False
            self.is_completed = False
            if not self.volunteer:
                raise ValidationError({'volunteer': 'Volunteer is required if delivery is in execution'})
        else:
            raise ValidationError({'volunteer': 'Invalid delivery status'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Task(models.Model):
    category = models.CharField(max_length=255, verbose_name='категория')
    name = models.CharField(max_length=255, verbose_name='название')
    price = models.PositiveIntegerField(verbose_name='часы')
    description = models.TextField(blank=True, null=True, verbose_name='описание')
    start_date = models.DateTimeField(verbose_name='дата начала')
    end_date = models.DateTimeField(verbose_name='дата конца')
    volunteers_needed = models.PositiveIntegerField(verbose_name='требуется волонтеров')
    volunteers_taken = models.PositiveIntegerField(verbose_name='волонтеров взяли', default=0)
    is_active = models.BooleanField(default=True, verbose_name='активная')
    is_completed = models.BooleanField(default=False, verbose_name='завершена')

    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True, verbose_name='город')
    curator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_curator', verbose_name='куратор')
    volunteers = models.ManyToManyField(User, blank=True, related_name='tasks', verbose_name='волонтеры')

    def __str__(self):
        return f'{self.name}, {self.start_date}'

    class Meta:
        verbose_name = 'задание'
        verbose_name_plural = 'задания'
