from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView

from events.models import Event

from .forms import EventRecruitmentForm
from .models import EventRecruitment

# Create your views here.


class Home(TemplateView):
    template_name = "recruitments/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        events = Event.objects.filter(status="参加者募集中")
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
        context["events"] = zip(events, recruitments)
        context["options"] = EventRecruitmentForm.Meta.model.PREFERENCE_CHOICES
        return context


class EventRecruitmentUpdate(UpdateView):
    """出欠掲示板のフォーム。GETリクエストは受け付けない"""

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
