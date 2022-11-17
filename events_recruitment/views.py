from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, UpdateView

from events.models import Event

from .forms import EventRecruitmentForm
from .models import EventRecruitment

# Create your views here.


class Home(TemplateView):
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
    success_url = reverse_lazy("recruitment:")

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
            return redirect("recruitment:")
        recruitment_form.event = event
        recruitment_form.member = self.request.user
        recruitment_form.save()
        messages.success(self.request, f"「{event}」の出欠を更新しました")
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        return redirect("recruitment:")


class EventRecruitmentList(ListView):
    model = EventRecruitment
    template_name = "recruitments/list.html"

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
        return context

    def get(self, request, *args, **kwargs):
        form = {}
        form["event"] = Event.objects.get(pk=self.kwargs["id"])
        form["m_eager"] = self.request.GET.getlist("eg")  # ◎
        form["m_yes"] = self.request.GET.getlist("yes")  # ○
        form["m_conditionally"] = self.request.GET.getlist("cd")  # △
        # ×と回答したメンバーにはさすがに打診できない
        temp = self.request.GET.get("temp") == "on"
        if temp:
            print("temp")
        return super().get(request, *args, **kwargs)
