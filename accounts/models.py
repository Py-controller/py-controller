from django.db import models
import uuid
from django.core.validators import MaxLengthValidator, MinLengthValidator


class ShiftOptions(models.TextChoices):
    CC = "Current account"
    CP = "Savings account"


class Account(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    account_number = models.CharField(
        max_length=20, validators=[MaxLengthValidator(20), MinLengthValidator(3)]
    )
    agency = models.CharField(
        max_length=5, validators=[MaxLengthValidator(5), MinLengthValidator(3)]
    )
    type = models.CharField(
        max_length=20, choices=ShiftOptions.choices, default=ShiftOptions.CC
    )
    code = models.CharField(
        max_length=3,
        validators=[MaxLengthValidator(3), MinLengthValidator(3)],
        null=True,
        default=None,
    )

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="accounts",
    )
    balance = models.DecimalField(
        max_digits=15,
        decimal_places=2,
    )
    overdraft_limit = models.DecimalField(
        max_digits=15,
        decimal_places=2,
    )
