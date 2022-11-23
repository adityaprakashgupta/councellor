from django.urls import path
from .views import GoogleLogin, googlecallback

urlpatterns = [
    path('dj-rest-auth/google/', GoogleLogin.as_view(), name='google_login'),
    path('google/callback', googlecallback, name="google_callback")
]