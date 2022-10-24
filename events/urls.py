"""EventsのURLを管理する"""
from django.urls import path

from .views import (
    EventCreate,
    EventDetail,
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
    path("update/<int:pk>/", EventUpdate.as_view(), name="event_update"),
    path("detail/<int:pk>/", EventDetail.as_view(), name="event_detail"),
    path("api/schools_get/", api_schools_get, name="api_schools_get"),
]
