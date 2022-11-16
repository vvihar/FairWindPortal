"""EventsのURLを管理する"""
from django.urls import path

from .views import EventRecruitmentList, EventRecruitmentUpdate, Home

app_name = "recruitment"

urlpatterns = [
    path("", Home.as_view(), name=""),
    path(
        "<int:id>/submit/", EventRecruitmentUpdate.as_view(), name="recruitment_update"
    ),
    path("<int:id>/list/", EventRecruitmentList.as_view(), name="recruitment_list"),
]
