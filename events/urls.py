"""EventsのURLを管理する"""
from django.urls import path

from events_accounting.views import (
    BillCreate,
    BillDelete,
    BillList,
    BillUpdate,
    download_bill,
    issue_bill,
)
from events_recruitment.views import (
    EventRecruitmentHome,
    EventRecruitmentList,
    EventRecruitmentUpdate,
    event_recruitment_csv,
)
from events_reflection.views import (
    EventReflectionList,
    EventReflectionTemplateCreateUpdate,
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
    # 出欠掲示板（events_recruitment）
    path("recruitments/", EventRecruitmentHome.as_view(), name="recruitment"),
    path(
        "<int:id>/recruit/list/event.csv", event_recruitment_csv, name="recruitment_csv"
    ),  # event.csvというファイルの実体がここにあるわけではない（URLのパターンを指定しているだけ）
    path(
        "<int:id>/recruit/",
        EventRecruitmentList.as_view(),
        name="recruitment_list",
    ),
    path(
        "<int:id>/recruit/submit/",
        EventRecruitmentUpdate.as_view(),
        name="recruitment_update",
    ),
    # 請求書（events_accounting）
    path("<int:id>/bill/create", BillCreate.as_view(), name="bill_create"),
    path("<int:id>/bill/", BillList.as_view(), name="bill_list"),
    path("<int:id>/bill/<int:pk>/update", BillUpdate.as_view(), name="bill_update"),
    path("<int:id>/bill/<int:pk>/delete", BillDelete.as_view(), name="bill_delete"),
    path("<int:id>/bill/<int:pk>/download", download_bill, name="bill_download"),
    path("<int:id>/bill/<int:pk>/issue", issue_bill, name="bill_issue"),
    # 振り返り（events_reflection）
    path("<int:id>/reflection/", EventReflectionList.as_view(), name="reflection_list"),
    path(
        "<int:id>/reflection/template/",
        EventReflectionTemplateCreateUpdate.as_view(),
        name="reflection_template",
    ),
]
