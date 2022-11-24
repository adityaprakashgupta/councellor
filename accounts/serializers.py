from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
import requests
from rest_framework import serializers
from rest_framework.settings import api_settings

User = get_user_model()


class UserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password')


class UserCreateSerializer(UserSerializer):

    def validate(self, attrs):
        email = attrs.get("email")
        res = requests.get("https://api.mailcheck.ai/email/" + email)
        if res.status_code == 200:
            if res.json()["disposable"]:
                return self.fail("email")

        return attrs

    def validate(self, attrs):
        user = User(**attrs)
        password = attrs.get("password")

        try:
            validate_password(password, user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error[api_settings.NON_FIELD_ERRORS_KEY]}
            )
        email = attrs.get("email")
        res = requests.get("https://api.mailcheck.ai/email/" + email)
        if res.status_code == 200:
            if res.json()["disposable"]:
                return self.fail("email")


        return attrs
