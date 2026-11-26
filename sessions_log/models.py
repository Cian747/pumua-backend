import uuid
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

from connection.base_models import UUIDModel
from practices.models import Technique


class SessionLog(UUIDModel):

    session_reference = models.UUIDField(default=uuid.uuid4,unique=True,editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="sessions")
    technique = models.ForeignKey(Technique,on_delete=models.PROTECT,related_name="completed_sessions")
    started_at = models.DateTimeField()
    completed_at = models.DateTimeField(null=True,blank=True)
    duration_seconds = models.PositiveIntegerField(default=0,validators=[MinValueValidator(0)])
    completed = models.BooleanField(default=False)

    class Meta:
        ordering = ["-started_at"]

        indexes = [
            models.Index(
                fields=["user", "started_at"]
            ),
            models.Index(
                fields=["user", "completed"]
            ),
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
