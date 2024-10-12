from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import RequestMessage
from notifications_app.models import Notification
from django.conf import settings
from django.core.mail import send_mail
from .models import Feedback


@receiver(post_save, sender=RequestMessage)
def create_feedback(sender, instance, created, **kwargs):
    if created:
        notification = Notification.objects.create(
            title=instance.type,
            text=f'Пользователь {instance.user.tg_username} оставил заявку "{instance.text}"',
            form=instance.form,
            created=timezone.now()
        )
        notification.save()



@receiver(post_save, sender=Feedback)
def send_feedback_notification(sender, instance, created, **kwargs):
    if created:
        subject = f"Новый отзыв от пользователя {instance.user}"
        message = (
            f"Тип отзыва: {instance.get_type_display()}\n"
            f"Текст: {instance.text}\n"
            f"Дата создания: {instance.created_at}\n"
            f"Пользователь: {instance.user.name}"
        )

        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [settings.ADMIN_EMAIL],
            fail_silently=False,
        )
