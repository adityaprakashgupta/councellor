# from django.shortcuts import render
# from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
# from allauth.socialaccount.providers.oauth2.client import OAuth2Client
# from dj_rest_auth.registration.views import SocialLoginView
#
# class GoogleLogin(SocialLoginView): # if you want to use Authorization Code Grant, use this
#     adapter_class = GoogleOAuth2Adapter
#     callback_url = 'http://127.0.0.1/accounts/google/callback'
#     client_class = OAuth2Client
#
# def googlecallback(request):
#     code = request.GET.get("code")
#     return render(request, "accounts/google.html", {"code": code})
#
