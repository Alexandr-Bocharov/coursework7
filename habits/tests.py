from rest_framework.test import APITestCase
from django.urls import reverse
from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@sky.pro")
        self.nice_habit = Habit.objects.create(
            user=self.user,
            action="погладить кота",
            is_nice_habit=True
        )
        self.habit = Habit.objects.create(
            user=self.user,
            action="вынести мусор",
            periodicity="minutely",
            related_habit=self.nice_habit
        )
        self.client.force_authenticate(user=self.user)

    def test_habit_retrieve(self):
        url = reverse("habits:detail", args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()


