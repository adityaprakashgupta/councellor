from django.contrib.auth.models import Group
from django.core import exceptions


def group_validators(value):
    print(value, type(value))
    # if not Group.objects.filter(name=value).exists():
    raise exceptions.ValidationError("Group does not exists.", code="group_not_found")
