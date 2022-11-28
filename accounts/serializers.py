from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import transaction
from djoser.conf import settings
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
import requests
from rest_framework import serializers
from rest_framework.settings import api_settings

User = get_user_model()


def check_temp_mail(email):
    res = requests.get("https://api.mailcheck.ai/email/" + email)
    if res.status_code == 200:
        if res.json()["disposable"]:
            raise django_exceptions.ValidationError("Use of disposable emails are not allowed",
                                                    code="disposable_email_not_allowed")
    return None


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)


class UserSerializer(UserCreateSerializer):
    groups = GroupSerializer(many=True, read_only=True)

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password', 'groups')


class UserCreateSerializer(UserSerializer):
    groups = serializers.ListField(child=serializers.CharField(), write_only=True)

    def validate(self, attrs):
        groups = attrs.pop("groups")
        user = User(**attrs)
        password = attrs.get("password")
        email = attrs.get("email")

        try:
            check_temp_mail(email)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"email": serializer_error[api_settings.NON_FIELD_ERRORS_KEY]}
            )
        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error[api_settings.NON_FIELD_ERRORS_KEY]}
            )
        try:
            for group in groups:
                if not Group.objects.filter(name=group).exists():
                    raise django_exceptions.ValidationError(f"Group with name {group} doesn't exists",
                                                            code="group_does_not_exists")
            attrs["groups"] = groups
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"groups": serializer_error[api_settings.NON_FIELD_ERRORS_KEY]}
            )

        return attrs

    def perform_create(self, validated_data):
        groups = validated_data.pop("groups")
        with transaction.atomic():
            user = User.objects.create_user(**validated_data)
            for group in groups:
                group_instance = Group.objects.filter(name=group)
                user.groups.set(group_instance)
            user.save()
            if settings.SEND_ACTIVATION_EMAIL:
                user.is_active = False
                user.save(update_fields=["is_active"])
        return user
