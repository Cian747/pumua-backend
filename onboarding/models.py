from django.db import models
from django.conf import settings
from connection.base_models import UUIDModel

class WellbeingProfile(UUIDModel):

    class Goals(models.TextChoices):
        RELAXATION = "relaxation", "Calm and relaxation"
        SLEEP = "sleep", "Better sleep"
        FOCUS = "focus", "Focus and energy"
        STRESS = "stress", "Stress relief"
        BREATH_CONTROL = "breath_control", "Breath control"
        GENERAL = "general", "General wellbeing"

    class Experience(models.TextChoices):
        BEGINNER = "beginner", "Beginner"
        OCCASIONAL = "occasional", "Occasional"
        REGULAR = "regular", "Regular"

    class Duration(models.TextChoices):
        FIVE = "5", "5 minutes"
        TEN = "10", "10 minutes"
        FIFTEEN = "15", "15 minutes"
        TWENTY = "20", "20 minutes or more"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="wellbeing_profile"
    )

    goals = models.JSONField(default=list)

    breathing_experience = models.CharField(
        max_length=20,
        choices=Experience.choices,
        default=Experience.BEGINNER
    )

    preferred_duration = models.CharField(
        max_length=10,
        choices=Duration.choices,
        default=Duration.FIVE
    )

    sleep_quality = models.PositiveSmallIntegerField(
        null=True,
        blank=True
    )

    stress_level = models.PositiveSmallIntegerField(
        null=True,
        blank=True
    )

    previous_experience = models.TextField(
        blank=True
    )

    completed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Wellbeing profile: {self.user.email}"
