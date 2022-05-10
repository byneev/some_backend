from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager

ROLES = (
    ("user", "user"),
    ("moderator", "moderator"),
    ("admin", "admin"),
    ("superuser", "superuser"),
)


class User(AbstractUser):
    role = models.CharField("Права", max_length=20, choices=ROLES)
    bio = models.TextField("Биография", blank=True)
    confirmation_code = models.CharField(
        "Код подтверждения", max_length=9, blank=True
    )

    objects = UserManager()
