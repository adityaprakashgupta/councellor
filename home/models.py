from django.db import models
from accounts.models import BaseModel, User
from .validators import group_validators


# Create your models here.
class Day(BaseModel):
    name = models.CharField(choices=[
        ("mon", "Monday"),
        ("tue", "Tuesday"),
        ("wed", "Wednesday"),
        ("fri", "Friday"),
        ("sat", "Saturday"),
        ("sun", "Sunday")
    ], max_length=3, unique=True)


class Slot(BaseModel):
    name = models.CharField(max_length=5)
    start_time = models.TimeField()
    end_time = models.TimeField()
    available_days = models.ManyToManyField("Day", on_delete=models.CASCADE)


class Service(BaseModel):
    name = models.CharField(unique=True)
    price = models.IntegerField(max_length=5, blank=False)
    price_on_holidays = models.IntegerField(max_length=5, blank=True)

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        if not self.price_on_holidays:
            if update_fields is None:
                update_fields = {"price_on_holidays"}
            self.price_on_holidays = self.price + self.price * (25 // 100)
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )


class Appointments(BaseModel):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    counsellor = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    slot = models.ForeignKey("Slot", on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
