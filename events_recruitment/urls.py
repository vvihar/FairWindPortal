"""EventsのURLを管理する"""
from django.urls import path

from .views import EventRecruitmentUpdate, Home

app_name = "recruitment"

urlpatterns = [
    path("", Home.as_view(), name=""),
    path(
        "submit/<int:id>/", EventRecruitmentUpdate.as_view(), name="recruitment_update"
    ),
]