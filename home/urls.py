from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import AppointmentViewSet

router = DefaultRouter()
router.register('appointments', AppointmentViewSet, basename='appointments')

urlpatterns = router.urls
