from rest_framework import serializers
from .models import Appointment, FreeSlot


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = "__all__"

    def validate(self, attrs):
        if not FreeSlot.objects.filter(date=attrs["date"], slots=attrs["slot"]).exists():
            raise serializers.ValidationError({"slot": "Slot is booked."})
        return attrs
