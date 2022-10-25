"""EventsのURLを管理する"""
from django.urls import path

from .views import (
    EventCancelInvitation,
    EventCreate,
    EventDetail,
    EventMakeInvitation,
    EventParticipants,
    EventReplyInvitation,
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
    path("<int:pk>/update/", EventUpdate.as_view(), name="event_update"),
    path("<int:pk>/", EventDetail.as_view(), name="event_detail"),
    path(
        "<int:pk>/participants/", EventParticipants.as_view(), name="event_participants"
    ),
    path(
        "<int:pk>/invite/",
        EventMakeInvitation.as_view(),
        name="event_invite",
    ),
    path(
        "<int:id>/invite/<int:pk>/cancel",
        EventCancelInvitation.as_view(),
        name="event_cancel_invitation",
    ),
    path(
        "<int:id>/invite/<int:pk>/reply",
        EventReplyInvitation.as_view(),
        name="event_reply_invitation",
    ),
    path("api/schools_get/", api_schools_get, name="api_schools_get"),
]
