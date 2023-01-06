from django.db import models
import uuid


class StartChoice(models.TextChoices):
    JANUARY = "January"
    FEBRUARY = "February"
    MARCH = "March"
    APRIL = "April"
    MAY = "May"
    JUNE = "June"
    JULY = "July"
    AUGUST = "August"
    SEPTEMBER = "September"
    OCTOBER = "October"
    NOVEMBER = "November"
    DECEMBER = "December"


class PlanningCycleChoice(models.TextChoices):
    MONTH = "Month"
    YEAR = "Year"


class Planning(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    start = models.CharField(choices=StartChoice.choices, max_length=10)
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
