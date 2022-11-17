"""EventsのURLを管理する"""
from django.urls import path

from .views import make_short_url, redirect_to

app_name = "shortener"

urlpatterns = [
    path("", make_short_url, name=""),
    path("<str:hashid>", redirect_to, name="redirect_to"),
]
