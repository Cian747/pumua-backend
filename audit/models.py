from django.db import models
from django.conf import settings

from connection.base_models import UUIDModel


class AuditLog(UUIDModel):

    actor = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="audit_events")
    action = models.CharField(max_length=100)
    object_type = models.CharField(max_length=100)
    object_id = models.CharField(max_length=100)
    metadata = models.JSONField(default=dict)
    occurred_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-occurred_at"]
        indexes = [
            models.Index(fields=["actor", "occurred_at"]),
            models.Index(fields=["action", "occurred_at"]),
        ]

    def __str__(self):
        return f"{self.action} - {self.object_type}"
