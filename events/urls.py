"""EventsのURLを管理する"""
from django.urls import path

from .views import (
    EventCreate,
    EventUpdate,
    Home,
    MakeSchoolDB,
    SchoolDetail,
    SchoolList,
    api_schools_get,
)

app_name = "events"

urlpatterns = [
    path("", Home.as_view(), name=""),
    path("school/db_update/", MakeSchoolDB.as_view(), name="db_update"),
    path("school/", SchoolList.as_view(), name="school_list"),
    path("school/<str:pk>/", SchoolDetail.as_view(), name="school_detail"),
    path("new/", EventCreate.as_view(), name="event_create"),
    path("edit/<int:pk>/", EventUpdate.as_view(), name="event_update"),
    path("api/schools_get/", api_schools_get, name="api_schools_get"),
]
