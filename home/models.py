from django.db import models
from accounts.models import BaseModel, User
from .validators import group_validators

# Create your models here.
class Appointments(BaseModel):
    client = models.ForeignKey(User, on_delete=models.CASCADE)

