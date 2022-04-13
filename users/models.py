from django.contrib.auth.models import AbstractUser
import uuid

from django.db import models


class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.ForeignKey(Role, on_delete=models.RESTRICT)

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
