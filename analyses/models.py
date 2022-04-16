from django.db import models
from samples.models import Sample, User, Lab, Tool
import uuid


class Analysis(models.Model):
    class Status(models.TextChoices):
        FINISHED = "FINISHED"
        PENDING = "PENDING"
        IN_PROGRESS = "IN_PROGRESS"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sample = models.ForeignKey(
        Sample, on_delete=models.RESTRICT, null=True, related_name="analysis"
    )  # So we can do Sample.analysis
    laborant = models.ForeignKey(
        User, on_delete=models.RESTRICT, null=True, related_name="analyses"
    )
    lab = models.ForeignKey(
        Lab, on_delete=models.RESTRICT, null=True, related_name="analysis"
    )
    status = models.CharField(max_length=12, choices=Status.choices)
    structure = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True)
    ended_at = models.DateTimeField(null=True)
    tools = models.ManyToManyField(Tool, related_name="analysis")
