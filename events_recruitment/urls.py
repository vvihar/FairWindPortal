"""EventsのURLを管理する"""
from django.urls import path

from .views import home

app_name = "recruitment"

urlpatterns = [
    path("", home, name=""),
]
