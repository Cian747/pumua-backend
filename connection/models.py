import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager


class User(AbstractUser):

    class Roles(models.TextChoices):
        PARTICIPANT = "participant", "Participant"
        COACH = "coach", "Coach"
        ADMIN = "admin", "Admin"

    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    username = None
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20,choices=Roles.choices,default=Roles.PARTICIPANT)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


import uuid

from django.db import models


class UUIDModel(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
