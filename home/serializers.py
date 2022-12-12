from rest_framework import serializers
from rest_framework.settings import api_settings
from accounts.models import User
from .models import Appointment
from django.core import exceptions as django_exceptions
from .validators import group_validators


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"

    def validate(self, attrs):
        counsellor = User.objects.get(pk=attrs.pop("counsellor"))
        user = self.context["request"].user
        for u_instances in [{"user": user, "group": "client"}, {"user": counsellor, "group": "counsellor"}]:
            try:
                group_validators(u_instances["user"], u_instances["group"])
            except django_exceptions.ValidationError as e:
                serializer_error = serializers.as_serializer_error(e)
                raise serializers.ValidationError(
                    {"user": serializer_error[api_settings.NON_FIELD_ERRORS_KEY]}
                )

    def create(self, validated_data):
        counsellor = validated_data.pop("counsellor")
        return super().create(validated_data)
