from django.db import models
from django.conf import settings
from connection.base_models import UUIDModel
from practices.models import Technique


class SessionLog(UUIDModel):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="sessions")
    technique = models.ForeignKey(Technique,on_delete=models.PROTECT,related_name="completed_sessions")
    duration_seconds = models.PositiveIntegerField()
    completed_at = models.DateTimeField()
    completed = models.BooleanField(default=False)

    class Meta:
        ordering = ["-completed_at"]
        indexes = [
            models.Index(fields=["user", "completed_at"]),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.duration_seconds}s"

class MonthlyGoal(UUIDModel):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="monthly_goals")
    year = models.PositiveSmallIntegerField()
    month = models.PositiveSmallIntegerField()
    target_sessions = models.PositiveSmallIntegerField(default=20)

    class Meta:
        ordering = ["-year", "-month"]

        constraints = [
            models.UniqueConstraint(
                fields=["user", "year", "month"],
                name="unique_user_monthly_goal"
            )
        ]

    def __str__(self):
        return (
            f"{self.user.email} - "
            f"{self.year}/{self.month}"
        )
