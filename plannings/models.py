from django.db import models
import uuid


class StartChoice(models.IntegerChoices):
    JAN = 1
    FEB = 2
    MAR = 3
    APR = 4
    MAY = 5
    JUN = 6
    JUL = 7
    AUG = 8
    SEP = 9
    OCT = 10
    NOV = 11
    DEC = 12


class PlanningCycleChoice(models.TextChoices):
    MONTH = "Month"
    YEAR = "Year"


class Planning(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    start = models.IntegerField(choices=StartChoice.choices)
    planning_cycle = models.CharField(
        choices=PlanningCycleChoice.choices, max_length=10
    )
    number_of_cycles = models.PositiveIntegerField(default=1)
    expense = models.DecimalField(max_digits=15, decimal_places=2, null=False)
    account = models.ForeignKey(
        "accounts.Account",
        on_delete=models.CASCADE,
        related_name="plannings",
    )
    category = models.ForeignKey(
        "categories.Categories",
        on_delete=models.CASCADE,
        related_name="planning",
    )
