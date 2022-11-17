"""EventsのURLを管理する"""
from django.urls import path

from events_recruitment.views import (
    EventRecruitmentHome,
    EventRecruitmentList,
    EventRecruitmentUpdate,
)

from .views import (
    EventCancelInvitation,
    EventCreate,
    EventDetail,
    EventListAll,
    EventMakeInvitation,
    EventParticipants,
    EventReplyInvitation,
    EventUpdate,
    Home,
)

app_name = "events"

urlpatterns = [
    path("", Home.as_view(), name=""),
    path("all/", EventListAll.as_view(), name="event_list_all"),
    path("new/", EventCreate.as_view(), name="event_create"),
    path("<int:pk>/update/", EventUpdate.as_view(), name="event_update"),
    path("<int:pk>/", EventDetail.as_view(), name="event_detail"),
    path(
        "<int:pk>/participants/", EventParticipants.as_view(), name="event_participants"
    ),
    path(
        "<int:id>/invite/",
        EventMakeInvitation.as_view(),
        name="event_invite",
    ),
    path(
        "<int:id>/invite/<int:pk>/cancel",
        EventCancelInvitation.as_view(),
        name="event_cancel_invitation",
    ),
    path(
        "<int:id>/invite/reply",
        EventReplyInvitation.as_view(),
        name="event_reply_invitation",
    ),
    path("recruitments/", EventRecruitmentHome.as_view(), name="recruitment"),
    path(
        "<int:id>/recruit/submit/",
        EventRecruitmentUpdate.as_view(),
        name="recruitment_update",
    ),
    path(
        "<int:id>/recruit/list/",
        EventRecruitmentList.as_view(),
        name="recruitment_list",
    ),
]
