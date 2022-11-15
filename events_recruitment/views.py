from django import forms
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView

from events.models import Event

from .forms import EventRecruitmentForm
from .models import EventRecruitment

# Create your views here.


class Home(TemplateView):
    template_name = "recruitments/index.html"


class EventRecruitmentUpdate(UpdateView):
    """出欠掲示板のフォーム"""

    template_name = "recruitments/form.html"
    model = EventRecruitment
    form_class = EventRecruitmentForm
    success_url = reverse_lazy("recruitment:")

    def get_object(self):
        event = Event.objects.get(pk=self.kwargs["pk"])
        try:
            return EventRecruitment.objects.get(event=event, member=self.request.user)
        except EventRecruitment.DoesNotExist:
            return EventRecruitment(event=event, member=self.request.user)

    # TODO: method を POST のみに限定し、送信自体はメインページから行うようにする
