from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from habits.models import Habit
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@sky.pro")
        self.nice_habit = Habit.objects.create(
            user=self.user, action="погладить кота", is_nice_habit=True
        )
        self.habit = Habit.objects.create(
            user=self.user,
            action="вынести мусор",
            periodicity="minutely",
            related_habit=self.nice_habit,
        )
        self.published_habit = Habit.objects.create(
            user=self.user, action="подтягивания", reward="сок", is_published=True
        )
        self.published_nice_habit = Habit.objects.create(
            user=self.user, action="погладить cобаку", is_nice_habit=True, is_published=True
        )
        self.client.force_authenticate(user=self.user)

    def test_habit_retrieve(self):
        url = reverse("habits:detail", args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), self.habit.action)
        self.assertEqual(data.get("related_habit"), self.nice_habit.id)

    def test_habit_update(self):
        url = reverse("habits:update", args=(self.habit.pk,))
        data = {"action": "отжимания"}
        response = self.client.patch(url, data)
        # print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("action"), data.get("action"))

    def test_habit_delete(self):
        url = reverse("habits:delete", args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 3)

    def test_habit_useful_list(self):
        url = reverse("habits:useful-list")
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            data.get("results")[0].get("action"),
            self.habit.action
        )

    def test_habit_nice_list(self):
        url = reverse("habits:nice-list")
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            data.get("results")[0].get("action"),
            self.nice_habit.action
        )

    def test_public_habit_useful_list(self):
        url = reverse("habits:public-useful-list")
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            data.get("results")[0].get("action"),
            self.published_habit.action
        )

