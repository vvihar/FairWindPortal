"""contactのURLを管理する"""
from django.urls import path

from .views import (
    ContactCreate,
    ContactLinkToEvent,
    ContactList,
    ContactThreadList,
    ContactThreadPost,
    ContactThreadUpdate,
    ContactUpdate,
)

app_name = "contact"

urlpatterns = [
    path("", ContactList.as_view(), name=""),
    path("create/", ContactCreate.as_view(), name="thread_create"),
    path("<int:pk>/", ContactThreadList.as_view(), name="thread"),
    path("<int:pk>/update/", ContactUpdate.as_view(), name="thread_update"),
    path(
        "<int:pk>/link_to_event/",
        ContactLinkToEvent.as_view(),
        name="thread_link_to_event",
    ),
    path("<int:pk>/post/", ContactThreadPost.as_view(), name="message_post"),
    path(
        "<int:pk>/post/<int:id>/",
        ContactThreadUpdate.as_view(),
        name="message_update",
    ),
]
