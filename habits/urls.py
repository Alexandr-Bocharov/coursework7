from habits.apps import HabitsConfig
from django.urls import path
from habits.views import (
    UsefulHabitListAPIView,
    NiceHabitListAPIView,
    HabitCreateAPIView,
    PublicUsefulHabitListAPIView,
    PublicNiceHabitListAPIView,
    HabitUpdateAPIView,
    HabitDestroyAPIView,
    HabitRetrieveAPIView,
)

app_name = HabitsConfig.name

urlpatterns = [
    path("useful_list/", UsefulHabitListAPIView.as_view(), name="useful-list"),
    path("nice_list/", NiceHabitListAPIView.as_view(), name="nice-list"),
    path("create/", HabitCreateAPIView.as_view(), name="create"),
    path("public_useful_list/", PublicUsefulHabitListAPIView.as_view(), name="public-useful-list"),
    path("public_nice_list/", PublicNiceHabitListAPIView.as_view(), name="public-nice-list"),
    path("<int:pk>/update/", HabitUpdateAPIView.as_view(), name="update"),
    path("<int:pk>/delete/", HabitDestroyAPIView.as_view(), name="delete"),
    path("<int:pk>/detail/", HabitRetrieveAPIView.as_view(), name='detail'),
]
