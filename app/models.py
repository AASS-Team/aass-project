from django.db import models
import uuid

from users.models import User
from labs.models import Lab
from tools.models import Tool
from grants.models import Grant


class Sample(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    grant = models.ForeignKey(Grant, on_delete=models.RESTRICT, null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    note = models.CharField(max_length=255, blank=True)
    amount = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
