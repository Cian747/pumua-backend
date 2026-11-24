
from django.db import models

from connection.base_models import UUIDModel


class PracticeCategory(UUIDModel):

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to="practice_categories/",null=True,blank=True)

    is_active = models.BooleanField(default=True)

    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "name"]

    def __str__(self):
        return self.name


class Technique(UUIDModel):

    category = models.ForeignKey(
        PracticeCategory,
        on_delete=models.PROTECT,
        related_name="techniques"
    )

    name = models.CharField(max_length=150)
    description = models.TextField()
    timing_pattern = models.JSONField(default=dict)
    duration_minutes = models.PositiveSmallIntegerField()
    instructions = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["duration_minutes", "name"]

    def __str__(self):
        return self.name
