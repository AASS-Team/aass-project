from django.db import models
from samples.models import Sample, User, Lab, Tool
import uuid


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
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True)
    ended_at = models.DateTimeField(null=True)
    tools = models.ManyToManyField(Tool)
