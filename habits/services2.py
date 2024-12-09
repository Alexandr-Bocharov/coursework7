from datetime import timedelta

from django.utils.timezone import now
from django_celery_beat.models import PeriodicTask, IntervalSchedule, ClockedSchedule
import json

from habits.models import Habit


def schedule_habit_task(habit: Habit):
    """
    Создает или обновляет расписание задачи для привычки.
    """
    tg_time = habit.tm

    hours = tg_time.hour
    minutes = tg_time.minute
    seconds = tg_time.second
    noww = now() + timedelta(hours=3)

    target_time = noww.replace(hour=hours, minute=minutes, second=seconds, microsecond=0)
    print(target_time)
    if target_time < noww:
        target_time += timedelta(days=1)
    print(target_time)
    print(type(target_time))
    # Конвертируем периодичность привычки в интервал
    interval_mapping = {
        "minutely": {"every": 1, "period": IntervalSchedule.MINUTES},
        "hourly": {"every": 1, "period": IntervalSchedule.HOURS},
        "daily": {"every": 1, "period": IntervalSchedule.DAYS},
        "weekly": {"every": 7, "period": IntervalSchedule.DAYS},
    }

    periodicity = interval_mapping.get(habit.periodicity)

    schedule, created = IntervalSchedule.objects.get_or_create(
        every=periodicity["every"],
        period=periodicity["period"],
    )

    task = PeriodicTask.objects.create(
        name=f"send_tg_message_{habit.id}",
        interval=schedule,
        # start_time=target_time,
        task="habits.tasks.send_tg_message",
        args=json.dumps([habit.id])
    )
    task.save()

