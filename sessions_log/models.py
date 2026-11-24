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
