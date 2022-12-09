from django.db import models
from accounts.models import BaseModel, User


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
    available_days = models.ManyToManyField("Day")


class Service(BaseModel):
    name = models.CharField(unique=True, max_length=225)
    price = models.PositiveIntegerField(blank=False)
    price_on_holidays = models.PositiveIntegerField(blank=True)
    category = models.CharField(max_length=225, choices=[
        ("regular", "Regular"),
        ('pack', 'Pack')
    ])

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


class Appointment(BaseModel):
    name = models.CharField(max_length=225, blank=True)
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointments_client")
    counsellor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointments_counsellor")
    date = models.DateField()
    slot = models.ForeignKey("Slot", on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    session_type = models.CharField(choices=[
        ("individual", "Individual"),
        ("group", "Group")
    ], default="individual", max_length=10)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )
        free_slots, created = FreeSlot.objects.get_or_create(counsellor=self.counsellor, date=self.date)
        if created:
            Slot.objects.filter()


class ServicePack(BaseModel):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="service_pack_client")
    counsellor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="service_pack_counsellor")
    no_of_members = models.PositiveIntegerField(default=1)
    no_grp_session = models.PositiveIntegerField(default=0)
    no_ind_session = models.PositiveIntegerField(default=1)
    appointments = models.ManyToManyField("Appointment")
    service = models.ForeignKey("Service", on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)

    def get_total_session(self):
        return self.no_grp_session + self.no_ind_session


class Leave(BaseModel):
    date = models.DateField()
    slots = models.ManyToManyField(Slot)
    counsellor = models.ForeignKey(User, on_delete=models.CASCADE)


class FreeSlot(BaseModel):
    counsellor = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    slots = models.ManyToManyField(Slot)
