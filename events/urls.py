"""EventsのURLを管理する"""
from django.urls import path

from .views import Home, MakeSchoolDB, SchoolDetail, SchoolList

app_name = "events"

urlpatterns = [
    path("", Home.as_view(), name=""),
    path("school/db_update/", MakeSchoolDB.as_view(), name="db_update"),
    path("school/", SchoolList.as_view(), name="school_list"),
    path("school/<str:pk>/", SchoolDetail.as_view(), name="school_detail"),
]
