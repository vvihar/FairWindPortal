"""contactのURLを管理する"""
from django.urls import path

from .views import (
    ContactCreate,
    ContactList,
    ContactThreadList,
    ContactThreadPost,
    ContactThreadUpdate,
    ContactUpdate,
)

app_name = "contact"

urlpatterns = [
    path("", ContactList.as_view(), name=""),
    path("create/", ContactCreate.as_view(), name="contact_create"),
    path("<int:pk>/", ContactThreadList.as_view(), name="thread"),
    path("<int:pk>/update/", ContactUpdate.as_view(), name="contact_update"),
    path("<int:pk>/post/", ContactThreadPost.as_view(), name="thread_create"),
    path(
        "<int:pk>/post/<int:id>/",
        ContactThreadUpdate.as_view(),
        name="thread_update",
    ),
]
