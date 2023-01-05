from django.db import models
import uuid


class ShiftOptions(models.TextChoices):
    CC = "Current account"
    CP = "Savings account"


class Account(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    account_number = models.CharField(max_length=9)
    agency = models.CharField(max_length=4)
    type = models.CharField(
        max_length=20, choices=ShiftOptions.choices, default=ShiftOptions.CC
    )
    code = models.CharField(max_length=5,null=True, default=None)

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
