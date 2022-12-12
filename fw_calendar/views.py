import datetime
import uuid

from accounts.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.timezone import make_aware
from django.views import generic
from events.models import Event
from icalendar import Calendar as IcsCalendar
from icalendar import Event as IcsEvent

from . import mixins
from .forms import ScheduleForm, SimpleScheduleForm
from .models import Schedule

# Create your views here.


class MonthCalendar(mixins.MonthCalendarMixin, generic.TemplateView):
    """月間カレンダーを表示するビュー"""

    template_name = "calendar/month.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context


class WeekCalendar(mixins.WeekCalendarMixin, generic.TemplateView):
    """週間カレンダーを表示するビュー"""

    template_name = "calendar/week.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_week_calendar()
        context.update(calendar_context)
        return context


class WeekWithScheduleCalendar(mixins.WeekWithScheduleMixin, generic.TemplateView):
    """スケジュール付きの週間カレンダーを表示するビュー"""

    template_name = "calendar/week_with_schedule.html"
    model = Schedule
    date_field = "date"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_week_calendar()
        context.update(calendar_context)
        return context


class MonthWithScheduleCalendar(mixins.MonthWithScheduleMixin, generic.TemplateView):
    """スケジュール付きの月間カレンダーを表示するビュー"""

    template_name = "calendar/month_with_schedule.html"
    model = Schedule
    date_field = "date"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        calendar_context = self.get_month_calendar()
        context.update(calendar_context)
        return context


class MyCalendar(mixins.MonthWithScheduleMixin, generic.CreateView):
    """月間カレンダー、週間カレンダー、スケジュール登録画面のある欲張りビュー"""

    template_name = "calendar/mycalendar.html"
    model = Schedule
    date_field = "date"
    form_class = ScheduleForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        month_calendar_context = self.get_month_calendar()
        context.update(month_calendar_context)
        month, year, day = (
            self.kwargs.get("month"),
            self.kwargs.get("year"),
            self.kwargs.get("day"),
        )
        if month and year and day:
            date = datetime.date(year=int(year), month=int(month), day=int(day))
        else:
            date = datetime.date.today()
        context["selected_date"] = date
        return context

    def form_valid(self, form):
        month = self.kwargs.get("month")
        year = self.kwargs.get("year")
        day = self.kwargs.get("day")
        if month and year and day:
            date = datetime.date(year=int(year), month=int(month), day=int(day))
        else:
            date = datetime.date.today()
        schedule = form.save(commit=False)
        schedule.date = date
        schedule.save()
        return redirect(
            "calendar:mycalendar", year=date.year, month=date.month, day=date.day
        )

    def get_initial(self):
        start_time = datetime.datetime.strftime(datetime.datetime.now(), "%H:%M")
        end_time = datetime.datetime.strftime(
            datetime.datetime.now() + datetime.timedelta(hours=1), "%H:%M"
        )
        if end_time < start_time:
            end_time = datetime.time.strftime(datetime.time(23, 59), "%H:%M")
        return {"start_time": start_time, "end_time": end_time}


class MonthWithFormsCalendar(mixins.MonthWithFormsMixin, generic.View):
    """フォーム付きの月間カレンダーを表示するビュー"""

    template_name = "calendar/month_with_forms.html"
    model = Schedule
    date_field = "date"
    form_class = SimpleScheduleForm

    def get(self, request, **kwargs):
        context = self.get_month_calendar()
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        # FIXME: 時刻を設定できるようにする
        context = self.get_month_calendar()
        formset = context["month_formset"]
        if formset.is_valid():
            formset.save()
            return redirect("calendar:month_with_forms")

        return render(request, self.template_name, context)


class CalendarIntegration(generic.TemplateView):
    template_name = "calendar/integration.html"

    def post(self, request, **kwargs):
        user = request.user
        user.calendar_uuid = uuid.uuid4()
        user.save()
        messages.success(request, "照会カレンダーのURLをリセットしました")
        return redirect("calendar:integration")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["calendar_uuid"] = user.calendar_uuid
        return context


def delete_schedule(request, **kwargs):
    """スケジュールを削除する"""

    schedule_id = kwargs.get("pk")
    schedule = get_object_or_404(Schedule, id=schedule_id)
    schedule.delete()
    return redirect(request.META.get("HTTP_REFERER"))


def ics_calendar(request, **kwargs):
    """スケジュールをiCalendar形式でダウンロードする"""

    response = HttpResponse(
        content_type="text/calendar",
        headers={"Content-Disposition": 'attachment; filename="fwcal.ics"'},
    )

    calendar_uuid = kwargs.get("uuid")
    user = get_object_or_404(User, calendar_uuid=calendar_uuid)

    cal = IcsCalendar()  # Calendarクラスをインスタンス化
    cal.add("prodid", "-//MyFWCalendar//MyFWCalendar//EN")
    cal.add("version", "2.0")
    cal.add("method", "PUBLISH")
    cal.add("x-wr-calname", "FairWind")
    cal.add("x-wr-caldesc", "FairWindのカレンダー")
    cal.add("x-wr-timezone", "Asia/Tokyo")

    # get all schedules after a year ago before a year later
    schedules = Schedule.objects.filter(
        date__gte=datetime.date.today() - datetime.timedelta(days=365),
        date__lte=datetime.date.today() + datetime.timedelta(days=365),
    )
    # get all events starting after a year ago and ending before a year later
    events = Event.objects.filter(
        start_datetime__gte=make_aware(datetime.datetime.now())
        - datetime.timedelta(days=365),
        end_datetime__lte=make_aware(datetime.datetime.now())
        + datetime.timedelta(days=365),
    )
    for schedule in schedules:
        event = IcsEvent()  # Eventクラスをインスタンス化
        event.add("summary", schedule.summary)
        start_datetime = datetime.datetime.combine(schedule.date, schedule.start_time)
        end_datetime = datetime.datetime.combine(schedule.date, schedule.end_time)
        event.add("dtstart", make_aware(start_datetime))
        event.add("dtend", make_aware(end_datetime))
        event.add("description", schedule.description)
        cal.add_component(event)
    for fw_event in events:
        event = IcsEvent()  # Eventクラスをインスタンス化
        event.add("summary", fw_event.name)
        event.add("dtstart", fw_event.start_datetime)
        event.add("dtend", fw_event.end_datetime)
        event.add("location", fw_event.venue)
        cal.add_component(event)
    response.write(cal.to_ical())
    return response
