
from django.urls import path

from .views import (
    SessionListCreateView,
    SessionDetailView,
    ProgressOverviewView,
    WeeklyProgressView,
    MonthlyProgressView,
    MonthlyGoalView,
)

urlpatterns = [
    path("sessions/", SessionListCreateView.as_view(), name="session-list"),
    path("sessions/<uuid:pk>/", SessionDetailView.as_view(), name="session-detail"),

    path("progress/overview/", ProgressOverviewView.as_view(), name="progress-overview"),
    path("progress/weekly/", WeeklyProgressView.as_view(), name="progress-weekly"),
    path("progress/monthly/", MonthlyProgressView.as_view(), name="progress-monthly"),

    path(
        "progress/goals/<int:year>/<int:month>/",
        MonthlyGoalView.as_view(),
        name="monthly-goal"
    ),
]
