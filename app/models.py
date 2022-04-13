from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

from labs.models import Lab
from tools.models import Tool


class Grant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)


class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.ForeignKey(Role, on_delete=models.RESTRICT)

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"


class Sample(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    grant = models.ForeignKey(Grant, on_delete=models.RESTRICT, null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    note = models.CharField(max_length=255, blank=True)
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)


class Analysis(models.Model):
    class Status(models.TextChoices):
        FINISHED = "Finished"
        PENDING = "Pending"
        IN_PROGRESS = "In progress"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sample = models.ForeignKey(Sample, on_delete=models.RESTRICT, null=True)
    laborant = models.ForeignKey(User, on_delete=models.RESTRICT, null=True)
    lab = models.ForeignKey(Lab, on_delete=models.RESTRICT, null=True)
    status = models.CharField(max_length=12, choices=Status.choices)
    structure = models.CharField(max_length=255, null=True)
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField()
    tools = models.ManyToManyField(Tool)
