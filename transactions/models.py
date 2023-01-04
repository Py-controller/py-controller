from django.db import models
import uuid


class TransactionTypes(models.TextChoices):
    PMT = "payment"
    RCT = "receipt"


class Transaction(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.CharField(max_length=255)
    transaction_type = models.CharField(
        max_length=7, choices=TransactionTypes.choices, default=TransactionTypes.RCT)
    transaction_date = models.DateField()
    """account = models.ForeignKey('accounts.Account', related_name='transactions')
    category = models.ForeignKey('categories.Category', related_name='transactions')"""
