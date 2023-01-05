from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import datetime


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    birthdate = models.DateField(default=datetime.date.today)
    cpf = models.CharField(max_length=14)
    # address = models.ForeignKey(
    #     "address.Address",
    #     on_delete=models.CASCADE,
    #     related_name="users",
    # )
