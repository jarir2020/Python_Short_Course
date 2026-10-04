"""URL routes for account endpoints."""

from django.urls import path

from accounts.controllers import LoginView, MeView, RegisterView


urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/me/", MeView.as_view(), name="me"),
]
