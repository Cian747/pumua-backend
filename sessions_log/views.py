from datetime import date, datetime, time, timedelta
from django.db.models.functions import TruncDate
from django.db.models import Sum, Count
from django.shortcuts import get_object_or_404
from django.utils import timezone

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SessionLog, MonthlyGoal
from .serializers import SessionLogSerializer, MonthlyGoalSerializer


def completed_sessions_for(user):
    return SessionLog.objects.filter(user=user, completed=True)


def get_streak(session_dates):
    """Count consecutive active days, allowing today or yesterday as the start."""
    today = timezone.localdate()

    if today in session_dates:
        current_day = today
    elif today - timedelta(days=1) in session_dates:
        current_day = today - timedelta(days=1)
    else:
        return 0

    streak = 0
    while current_day in session_dates:
        streak += 1
        current_day -= timedelta(days=1)

    return streak


class SessionListCreateView(generics.ListCreateAPIView):
    serializer_class = SessionLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return completed_sessions_for(self.request.user)

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            completed=True
        )


class SessionDetailView(generics.RetrieveAPIView):
    serializer_class = SessionLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return completed_sessions_for(self.request.user)


class ProgressOverviewView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        sessions = completed_sessions_for(request.user)

        today = timezone.localdate()
        month_start = today.replace(day=1)

        totals = sessions.aggregate(
            total_sessions=Count("id"),
            total_seconds=Sum("duration_seconds")
        )

        month_sessions = sessions.filter(
            completed_at__date__gte=month_start,
            completed_at__date__lte=today
        )

        month_total = month_sessions.count()

        goal = MonthlyGoal.objects.filter(
            user=request.user,
            year=today.year,
            month=today.month
        ).first()

        active_dates = set(
            sessions.values_list("completed_at__date", flat=True).distinct()
        )

        return Response({
            "total_sessions": totals["total_sessions"] or 0,
            "total_minutes": (totals["total_seconds"] or 0) // 60,
            "current_streak": get_streak(active_dates),
            "monthly_sessions": month_total,
            "monthly_goal": goal.target_sessions if goal else 20,
            "monthly_goal_progress": month_total,
        })


class WeeklyProgressView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        today = timezone.localdate()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)

        sessions = completed_sessions_for(request.user).filter(
            completed_at__date__gte=week_start,
            completed_at__date__lte=week_end
        )

        daily_totals = {
            row["day"]: row["total"]
            for row in (
                sessions
                .annotate(day=TruncDate("completed_at"))
                .values("day")
                .annotate(total=Count("id"))
            )
        }

        return Response([
            {
                "date": week_start + timedelta(days=offset),
                "sessions": daily_totals.get(
                    week_start + timedelta(days=offset), 0
                )
            }
            for offset in range(7)
        ])


class MonthlyProgressView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        today = timezone.localdate()

        try:
            year = int(request.query_params.get("year", today.year))
            month = int(request.query_params.get("month", today.month))
            month_start = date(year, month, 1)
        except (ValueError, TypeError):
            return Response(
                {"detail": "Provide a valid year and month."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if month == 12:
            next_month = date(year + 1, 1, 1)
        else:
            next_month = date(year, month + 1, 1)

        sessions = completed_sessions_for(request.user).filter(
            completed_at__date__gte=month_start,
            completed_at__date__lt=next_month
        )

        daily = (
            sessions.values("completed_at__date")
            .annotate(session_count=Count("id"))
            .order_by("completed_at__date")
        )

        return Response({
            "year": year,
            "month": month,
            "total_sessions": sessions.count(),
            "total_minutes": (
                sessions.aggregate(total=Sum("duration_seconds"))["total"] or 0
            ) // 60,
            "daily_activity": [
                {
                    "date": row["completed_at__date"],
                    "sessions": row["session_count"]
                }
                for row in daily
            ]
        })


class MonthlyGoalView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, year, month):
        goal = get_object_or_404(
            MonthlyGoal,
            user=request.user,
            year=year,
            month=month
        )
        return Response(MonthlyGoalSerializer(goal).data)

    def put(self, request, year, month):
        data = request.data.copy()
        data["year"] = year
        data["month"] = month

        existing = MonthlyGoal.objects.filter(
            user=request.user,
            year=year,
            month=month
        ).first()

        serializer = MonthlyGoalSerializer(
            existing,
            data=data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return Response(serializer.data)
