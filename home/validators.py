from django.core import exceptions


def group_validators(user, name):
    if not user.groups.filter(mame=name).exists():
        raise exceptions.ValidationError(f"User does not belongs to {name}", code="group_not_found")
