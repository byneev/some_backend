from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager

SIMPLE_USER = 1
MODERATOR = 2
ADMIN = 3
SUPERUSER = 4

ROLES = (
    (SIMPLE_USER, "user"),
    (MODERATOR, "moderator"),
    (ADMIN, "admin"),
    (SUPERUSER, "superuser"),
)


class User(AbstractUser):
    email = models.EmailField("Почта")
    password = models.CharField("Пароль", max_length=20, blank=True)
    role = models.SmallIntegerField("Права", choices=ROLES)
    bio = models.TextField("Биография", blank=True)
    confirmation_code = models.CharField(
        "Код подтверждения", max_length=9, blank=True
    )

    objects = UserManager()
