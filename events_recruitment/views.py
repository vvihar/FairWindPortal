import csv

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, UpdateView

from events.models import Event

from .forms import EventRecruitmentForm
from .models import EventRecruitment

# Create your views here.


class EventRecruitmentHome(TemplateView):
    """出欠掲示板の本体のページ"""

    template_name = "recruitments/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        events = Event.objects.filter(status="参加者募集中").order_by("start_datetime")
        recruitments = []
        for event in events:
            if self.request.user.pk in event.recruitment.values_list(
                "member", flat=True
            ):
                recruitments.append(
                    EventRecruitment.objects.get(event=event, member=self.request.user)
                )
            else:
                recruitments.append(None)
        has_answered = [recruitment is not None for recruitment in recruitments]
        context["events"] = zip(events, recruitments, has_answered)
        context["options"] = EventRecruitmentForm.Meta.model.PREFERENCE_CHOICES
        return context


class EventRecruitmentUpdate(UpdateView):
    """出欠掲示板の更新を受け付ける。GETリクエストは受け付けない"""

    model = EventRecruitment
    form_class = EventRecruitmentForm
    success_url = reverse_lazy("events:recruitment")

    def get_object(self):
        event = Event.objects.get(pk=self.kwargs["id"])
        try:
            return EventRecruitment.objects.get(event=event, member=self.request.user)
        except EventRecruitment.DoesNotExist:
            return EventRecruitment(event=event, member=self.request.user)

    def form_valid(self, form):
        recruitment_form = form.save(commit=False)
        event = Event.objects.get(pk=self.kwargs["id"])
        if event.status != "参加者募集中":
            messages.error(self.request, f"「{event}」は参加者募集期間外です")
            return redirect("events:recruitment")
        recruitment_form.event = event
        recruitment_form.member = self.request.user
        recruitment_form.save()
        messages.success(self.request, f"「{event}」の出欠を更新しました")
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        return redirect("events:recruitment")


class EventRecruitmentList(ListView):
    model = EventRecruitment
    template_name = "recruitments/list.html"
    # FIXME: すでに打診されたメンバーは別枠で表示する

    def get_queryset(self):
        event = Event.objects.get(pk=self.kwargs["id"])
        return EventRecruitment.objects.filter(event=event)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["event"] = Event.objects.get(pk=self.kwargs["id"])
        context["options"] = (
            ("yes", "○"),
            ("conditionally", "△"),
            ("no", "×"),
        )
        context["is_admin"] = self.request.user in context["event"].admin.all()
        context["hashid"] = self.request.GET.get("hashid")
        return context


def event_recruitment_csv(request, id):
    """出欠掲示板のCSVをダウンロードする"""

    event = Event.objects.get(pk=id)
    if request.user not in event.admin.all():
        return redirect("events:recruitment")
    response = HttpResponse(content_type="text/csv", charset="CP932")
    response["Content-Disposition"] = 'attachment; filename="event.csv"'
    writer = csv.writer(response)
    writer.writerow(["名前", "期", "科類", "学部", "学科", "出欠", "コメント"])
    for recruitment in EventRecruitment.objects.filter(event=event):
        writer.writerow(
            [
                recruitment.member.last_name + recruitment.member.first_name,
                recruitment.member.grade,
                recruitment.member.course,
                (str(recruitment.member.faculty) if recruitment.member.faculty else ""),
                (
                    str(recruitment.member.department)
                    if recruitment.member.department
                    else ""
                ),
                recruitment.get_preference_display(),
                recruitment.comment,
            ]
        )
    return response
