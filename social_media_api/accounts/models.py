from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.URLField(blank=True)  # simple starter choice
    followers = models.ManyToManyField(
        "self",
        symmetrical=False,
        related_name="following",
        blank=True,
    )

    def __str__(self):
        return self.username
