from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
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
            raise django_exceptions.ValidationError("Use of disposable emails are not allowed", code="disposable_email_not_allowed")
    return None

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)
class UserSerializer(UserCreateSerializer):
    groups = GroupSerializer(many=True)
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password', 'groups')


class UserCreateSerializer(UserSerializer):

    def validate(self, attrs):
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

        return attrs
