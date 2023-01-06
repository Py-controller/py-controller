from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from cpf_field.models import CPFField


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birthdate = models.DateField()
    cpf = CPFField()
    email = models.EmailField(max_length=200)
    # address = models.ForeignKey(
    #     "address.Address",
    #     on_delete=models.CASCADE,
    #     related_name="users",
    # )
