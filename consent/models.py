
from django.conf import settings
from django.db import models
from connection.base_models import UUIDModel


class ConsentRecord(UUIDModel):

    class ConsentTypes(models.TextChoices):
        VIDEO_REVIEW = "video_review", "Video review"
        DATA_PROCESSING = "data_processing", "Data processing"

    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="consent_records")
    consent_type = models.CharField(max_length=30,choices=ConsentTypes.choices)
    version = models.CharField(max_length=30)
    agreed = models.BooleanField(default=False)
    agreed_at = models.DateTimeField(null=True,blank=True)
    revoked_at = models.DateTimeField(null=True,blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "consent_type"]),
        ]

    def __str__(self):
        return f"{self.user.email} - {self.consent_type}"
