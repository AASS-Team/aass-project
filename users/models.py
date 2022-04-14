import uuid
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(
        unique=True,
        max_length=255,
        blank=False,
    )

    objects = UserManager()

    USERNAME_FIELD = "email"

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
