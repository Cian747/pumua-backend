from django.db import models
from connection.base_models import UUIDModel


class LibraryCategory(UUIDModel):

    name = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(max_length=120,unique=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Library Categories"
        ordering = ["display_order", "name"]

    def __str__(self):
        return self.name


class LibraryVideo(UUIDModel):

    category = models.ForeignKey(LibraryCategory,on_delete=models.PROTECT,related_name="videos")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    description = models.TextField()
    video_url = models.URLField(max_length=500)
    thumbnail_url = models.URLField(max_length=500,blank=True)
    duration_seconds = models.PositiveIntegerField()
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True,blank=True)

    class Meta:
        ordering = ["-published_at", "title"]
        indexes = [
            models.Index(fields=["category", "is_published"]),
        ]

    def __str__(self):
        return self.title
