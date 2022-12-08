from home.models import Day, Slot
from django.contrib.auth.models import Group
import datetime
import pytz

for group in ["client", "counsellor", "Admin"]:
    print(Group.objects.get_or_create(name=group))


for day in ["mon", "tue", "wed", "thu", "fri", "sat"]:
    print(Day.objects.get_or_create(name=day))

for slot in [
    {
        "name": "1st",
        "start_time": datetime.time(10, 0, 0, 0, pytz.timezone("Asia/Kolkata")),
        "end_time": datetime.time(11, 0, 0, 0, pytz.timezone("Asia/Kolkata")),
        "available_days": Day.objects.all()
    },
    {
        "name": "2nd",
        "start_time": datetime.time(11, 0, 0, 0, pytz.timezone("Asia/Kolkata")),
        "end_time": datetime.time(12, 0, 0, 0, pytz.timezone("Asia/Kolkata")),
        "available_days": Day.objects.all()
    },
    {
        "name": "3rd",
        "start_time": datetime.time(12, 0, 0, 0, pytz.timezone("Asia/Kolkata")),
        "end_time": datetime.time(13, 0, 0, 0, pytz.timezone("Asia/Kolkata")),
        "available_days": Day.objects.all()
    },
    {
        "name": "4th",
        "start_time": datetime.time(16, 0, 0, 0, pytz.timezone("Asia/Kolkata")),
        "end_time": datetime.time(17, 0, 0, 0, pytz.timezone("Asia/Kolkata")),
        "available_days": Day.objects.filter(name__in=["mon", "tue", "wed", "thu", "fri", "sat"])
    },
    {
        "name": "5th",
        "start_time": datetime.time(17, 0, 0, 0, pytz.timezone("Asia/Kolkata")),
        "end_time": datetime.time(18, 0, 0, 0, pytz.timezone("Asia/Kolkata")),
        "available_days": Day.objects.filter(name__in=["mon", "tue", "wed", "thu", "fri", "sat"])
    },
    {
        "name": "6th",
        "start_time": datetime.time(18, 0, 0, 0, pytz.timezone("Asia/Kolkata")),
        "end_time": datetime.time(19, 0, 0, 0, pytz.timezone("Asia/Kolkata")),
        "available_days": Day.objects.filter(name__in=["mon", "tue", "wed", "thu", "fri", "sat"])
    }
]:
    available_days = slot.pop("available_days")
    db_slot, created = Slot.objects.get_or_create(**slot)
    if created:
        db_slot.available_days.add(*available_days)
        db_slot.save()
    print((db_slot, created))
