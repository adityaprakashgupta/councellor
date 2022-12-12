from rest_framework.decorators import api_view, permission_classes
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.models import User
from .models import Slot, Appointment
from .serializers import AppointmentSerializer


# Create your views here.
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def make_appointment(request):
    if request.method == "POST":
        error = False
        errors = []
        name = request.POST.get("name", "")
        client = request.user
        counsellor = User.objects.filter(pk=request.POST.get("counsellor"))
        if counsellor.exists():
            if counsellor[0].groups.filter(name="counsellor").exists():
                counsellor = counsellor[0]
            else:
                error = True
                errors.append({"counsellor": "Counsellor not found."})
        else:
            error = True
            errors.append({"counsellor": "Counsellor not found."})

        if request.POST.get("date"):
            date = request.POST.get("date")
        else:
            error = True
            errors.append({"date": "Please Provide a Valid date."})
        slot = Slot.objects.filter(pk=request.POST.get("slot"))
        if slot.exists():
            slot = slot[0]
        else:
            error = True
            errors.append({"slot": "Slot not found."})
        session_type = request.POST.get("session_type")
        if session_type not in ["individual", "group"]:
            error = True
            errors.append({"session_type": "Invalid session type."})

        if error:
            return Response({"errors": errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            app = Appointment.objects.create(name=name, client=client, counsellor=counsellor, slot=slot, date=date,
                                             session_type=session_type)
            serializer = AppointmentSerializer(app, many=False)
            return Response(serializer.data)
    return None


class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.groups.filter(name="Client").exists():
            return Appointment.objects.filter(client=self.request.user)
        else:
            return Appointment.objects.filter(counsellor=self.request.user)
