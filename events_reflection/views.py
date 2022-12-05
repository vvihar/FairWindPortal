from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.views.generic.edit import FormMixin

from events.models import Event

from .forms import EventReflectionForm
from .models import EventReflection

# Create your views here.


class EventReflectionList(ListView, FormMixin):
    template_name = "reflections/list.html"
    form_class = EventReflectionForm

    def get_success_url(self):
        return reverse_lazy("events:reflection_list", kwargs={"id": self.kwargs["id"]})

    def get_queryset(self):
        return EventReflection.objects.filter(event=self.kwargs["id"]).order_by("user")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["event"] = Event.objects.get(pk=self.kwargs["id"])
        return context

    def form_valid(self, form):
        # TODO: テンプレを設定できるようにする
        message = form.cleaned_data["reflection"]
        event = self.get_context_data()["event"]
        try:
            event_reflection = EventReflection.objects.get(
                event=event, user=self.request.user
            )
            event_reflection.reflection = message
            event_reflection.save()
        except EventReflection.DoesNotExist:
            EventReflection.objects.create(
                event=event, user=self.request.user, reflection=message
            )
        return super().form_valid(form)

    def get_initial(self):
        try:
            event_reflection = EventReflection.objects.get(
                event=self.kwargs["id"], user=self.request.user
            )
            return {"reflection": event_reflection.reflection}
        except EventReflection.DoesNotExist:
            return {"reflection": ""}

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
