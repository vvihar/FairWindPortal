"""EventsのURLを管理する"""
from django.urls import path

from . import views

app_name = "calendar"

urlpatterns = [
    path("", views.MonthCalendar.as_view(), name="month"),
    path("month/<int:year>/<int:month>/", views.MonthCalendar.as_view(), name="month"),
    path("week/", views.WeekCalendar.as_view(), name="week"),
    path(
        "week/<int:year>/<int:month>/<int:day>/",
        views.WeekCalendar.as_view(),
        name="week",
    ),
    path(
        "week_with_schedule/",
        views.WeekWithScheduleCalendar.as_view(),
        name="week_with_schedule",
    ),
    path(
        "week_with_schedule/<int:year>/<int:month>/<int:day>/",
        views.WeekWithScheduleCalendar.as_view(),
        name="week_with_schedule",
    ),
    path(
        "month_with_schedule/",
        views.MonthWithScheduleCalendar.as_view(),
        name="month_with_schedule",
    ),
    path(
        "month_with_schedule/<int:year>/<int:month>/",
        views.MonthWithScheduleCalendar.as_view(),
        name="month_with_schedule",
    ),
    path("mycalendar/", views.MyCalendar.as_view(), name="mycalendar"),
    path(
        "mycalendar/<int:year>/<int:month>/<int:day>/",
        views.MyCalendar.as_view(),
        name="mycalendar",
    ),
    path(
        "month_with_forms/",
        views.MonthWithFormsCalendar.as_view(),
        name="month_with_forms",
    ),
    path(
        "month_with_forms/<int:year>/<int:month>/",
        views.MonthWithFormsCalendar.as_view(),
        name="month_with_forms",
    ),
    path("delete/<int:pk>/", views.delete_schedule, name="delete"),
    path("integration/", views.CalendarIntegration.as_view(), name="integration"),
    path("integration/<str:uuid>/", views.ics_calendar, name="ics"),
]
