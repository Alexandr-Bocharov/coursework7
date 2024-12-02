from django.shortcuts import render
from rest_framework import generics

from habits.models import Habit
from habits.paginators import CustomHabitPaginator
from habits.serializers import HabitSerializer


class HabitCreateAPIView(generics.CreateAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()

    def perform_create(self, serializer):
        habit = serializer.save(user=self.request.user)
        habit.save()


class HabitUpdateAPIView(generics.UpdateAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()


class HabitDestroyAPIView(generics.DestroyAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()


class UsefulHabitListAPIView(generics.ListAPIView):
    """ Список полезных привычек, которые создал текущий пользователь """
    serializer_class = HabitSerializer
    pagination_class = CustomHabitPaginator

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user, is_nice_habit=False)


class NiceHabitListAPIView(generics.ListAPIView):
    """ Список приятных привычек, которые создал текущий пользователь """
    serializer_class = HabitSerializer
    pagination_class = CustomHabitPaginator

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user, is_nice_habit=True)


class PublicUsefulHabitListAPIView(generics.ListAPIView):
    """ Список публичных полезных привычек """
    serializer_class = HabitSerializer

    def get_queryset(self):
        return Habit.objects.filter(is_published=True, is_nice_habit=False)


class PublicNiceHabitListAPIView(generics.ListAPIView):
    """ Список публичных приятных привычек """
    serializer_class = HabitSerializer

    def get_queryset(self):
        return Habit.objects.filter(is_published=True, is_nice_habit=True)
