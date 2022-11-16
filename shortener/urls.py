"""EventsのURLを管理する"""
from django.urls import path

from .views import MakeShortURL, redirect_to

app_name = "shortener"

urlpatterns = [
    path("", MakeShortURL.as_view(), name=""),
    path("<str:hashid>", redirect_to, name="redirect_to"),
]
