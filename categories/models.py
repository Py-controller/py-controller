from django.db import models
import uuid


class Categories(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.TextField(max_length=50, null=False)
