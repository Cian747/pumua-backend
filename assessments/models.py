from django.conf import settings
from django.db import models
from connection.base_models import UUIDModel


class Assessment(UUIDModel):

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SUBMITTED = "submitted", "Submitted"
        UNDER_REVIEW = "under_review", "Under review"
        APPROVED = "approved", "Approved"
        FEEDBACK_SENT = "feedback_sent", "Feedback sent"
        RESUBMISSION = "resubmission", "Resubmission required"

    participant = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="assessments")
    video_key = models.CharField(max_length=500,unique=True)
    status = models.CharField(max_length=30,choices=Status.choices,default=Status.SUBMITTED)
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"Assessment: {self.participant.email}"


class CoachFeedback(UUIDModel):

    class Decisions(models.TextChoices):
        APPROVED = "approved", "Approved"
        RESUBMISSION = "resubmission", "Resubmission required"
        FEEDBACK = "feedback", "Feedback provided"

    assessment = models.ForeignKey(Assessment,on_delete=models.PROTECT,related_name="feedback")
    coach = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT,related_name="coach_feedback")
    note = models.TextField()
    decision = models.CharField(max_length=30,choices=Decisions.choices)

    def __str__(self):
        return f"Feedback for {self.assessment_id}"
