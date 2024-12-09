from celery import shared_task

from habits.models import Habit
from habits.services import send_message


@shared_task
def send_tg_message_after_create(habit_id):
    habit = Habit.objects.get(pk=habit_id)
    user_chat_id = habit.user.tg_chat_id
    action = habit.action
    action = f"Я буду {action} "
    time_for_action = habit.tm

    if time_for_action:
        time_for_action = f"в {time_for_action} "
    else:
        time_for_action = ""

    place_for_action = habit.place

    if place_for_action:
        place_for_action = f"в {place_for_action} "
    else:
        place_for_action = ""

    message = action + time_for_action + place_for_action
    send_message(message, user_chat_id)


@shared_task
def send_tg_message(habit_id):
    """
    Задача для отправки сообщения в Telegram.
    """
    try:
        habit = Habit.objects.get(pk=habit_id)
        hb = habit.action
        periodicity = habit.periodicity
        place = habit.place
        reward = habit.reward
        related_habit = habit.related_habit
        if hb:
            hb = f"Привычка: {hb}\n"

        if place:
            hb += f"Место: {place}\n"

        if reward:
            hb += f"Награда: {reward}"

        if related_habit:
            hb += f"Приятная привычка: {related_habit}"

        print(f"принт перед отправкой сообщения для {habit.action}")
        send_message(hb, habit.user.tg_chat_id)
        print(f"Отправлено сообщение для привычки: {habit.action}")
    except Exception as e:
        print(f"Произошла ошибка в send_tg_message: {e}")

