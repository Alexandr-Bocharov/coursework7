from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Habit
from .services2 import schedule_habit_task
from django_celery_beat.models import PeriodicTask


@receiver(post_save, sender=Habit)
def manage_habit_schedule(sender, instance, created, **kwargs):
    """
    Обновляем расписание при сохранении привычки.
    """
    if created:
        schedule_habit_task(instance)
        # print(instance)
        # print(instance.id)


@receiver(post_delete, sender=Habit)
def delete_habit_schedule(sender, instance, **kwargs):
    """
    Удаляем расписание при удалении привычки.
    """
    PeriodicTask.objects.filter(name=f"send_tg_message_{instance.id}").delete()
