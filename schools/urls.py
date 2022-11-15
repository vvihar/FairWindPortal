"""EventsのURLを管理する"""
from django.urls import path

from .views import (
    MakeSchoolDB,
    SchoolDetailUpdate,
    SchoolDetailView,
    SchoolList,
    api_schools_get,
)

app_name = "schools"

urlpatterns = [
    path("", SchoolList.as_view(), name="school_list"),
    path("db_update/", MakeSchoolDB.as_view(), name="db_update"),
    path("<str:pk>/", SchoolDetailView.as_view(), name="school_detail"),
    path(
        "<str:pk>/update",
        SchoolDetailUpdate.as_view(),
        name="school_detail_update",
    ),
    path("api/schools_get/", api_schools_get, name="api_schools_get"),
]
