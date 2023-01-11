from django.db import models
import uuid
from django.core.validators import MaxLengthValidator, MinLengthValidator


class Address(models.Model):
    
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    street = models.CharField(max_length=80)
    zip_code = models.CharField(max_length=8, validators=[MinLengthValidator(8), MaxLengthValidator(8)])
    district = models.CharField(max_length=20)
    city = models.CharField(max_length=80)
    number = models.IntegerField()
    state = models.CharField(max_length=50)
