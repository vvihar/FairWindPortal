"""AccountsのURLを管理する"""
from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (
    DivisionCreate,
    DivisionDelete,
    DivisionList,
    DivisionUpdate,
    GroupCreate,
    GroupDelete,
    GroupList,
    GroupUpdate,
    Home,
    Login,
    PasswordChange,
    UserImport,
    UserList,
    UserSignUp,
    UserUpdate,
    api_members_get,
)

app_name = "accounts"

urlpatterns = [
    path("", Home.as_view(), name=""),
    path("signup/", UserSignUp.as_view(), name="signup"),
    path("update/", UserUpdate.as_view(), name="update"),
    path(
        "password_change/",
        PasswordChange.as_view(),
        name="password_change",
    ),
    path("login/", Login.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path(
        "group/",
        GroupList.as_view(),
        name="group",
    ),
    path(
        "group/new/",
        GroupCreate.as_view(),
        name="group_create",
    ),
    path(
        "group/<int:pk>/delete/",
        GroupDelete.as_view(),
        name="group_delete",
    ),
    path(
        "group/<int:pk>/edit/",
        GroupUpdate.as_view(),
        name="group_update",
    ),
    path(
        "division/",
        DivisionList.as_view(),
        name="division",
    ),
    path(
        "division/new/",
        DivisionCreate.as_view(),
        name="division_create",
    ),
    path(
        "division/<int:pk>/delete/",
        DivisionDelete.as_view(),
        name="division_delete",
    ),
    path(
        "division/<int:pk>/edit/",
        DivisionUpdate.as_view(),
        name="division_update",
    ),
    path(
        "users/",
        UserList.as_view(),
        name="users",
    ),
    path(
        "users/import/",
        UserImport.as_view(),
        name="users_import",
    ),
    path("api/members_get/", api_members_get, name="api_members_get"),
]
