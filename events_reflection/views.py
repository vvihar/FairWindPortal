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
from events.views import OnlyEventAdminMixin

from .forms import EventReflectionForm
from .models import EventReflection, EventReflectionGeneral, EventReflectionTemplate

# Create your views here.


class EventReflectionList(ListView, FormMixin):
    # TODO: 企画の参加者のみ
    template_name = "reflections/list.html"
    form_class = EventReflectionForm

    def get_success_url(self):
        return reverse_lazy("events:reflection_list", kwargs={"id": self.kwargs["id"]})

    def get_queryset(self):
        return EventReflection.objects.filter(event=self.kwargs["id"]).order_by("user")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["event"] = Event.objects.get(pk=self.kwargs["id"])
        try:
            context["template"] = EventReflectionTemplate.objects.get(
                event=self.kwargs["id"]
            )
        except EventReflectionTemplate.DoesNotExist:
            context["template"] = None
        return context

    def form_valid(self, form):
        message = form.cleaned_data["reflection"]
        event = self.get_context_data()["event"]
        try:
            event_reflection = EventReflection.objects.get(
                event=event, user=self.request.user
            )
            if not message:
                event_reflection.delete()
            else:
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
            try:
                event_template = EventReflectionTemplate.objects.get(
                    event=self.kwargs["id"]
                )
                return {"reflection": event_template.reflection}
            except EventReflectionTemplate.DoesNotExist:
                return {"reflection": ""}

    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class EventReflectionTemplateCreateUpdate(OnlyEventAdminMixin, UpdateView):
    template_name = "reflections/edit_template.html"
    model = EventReflectionTemplate
    fields = ("reflection",)

    def get_success_url(self):
        return reverse_lazy("events:reflection_list", kwargs={"id": self.kwargs["id"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["event"] = Event.objects.get(pk=self.kwargs["id"])
        return context

    def get_object(self, queryset=None):
        try:
            return EventReflectionTemplate.objects.get(event=self.kwargs["id"])
        except EventReflectionTemplate.DoesNotExist:
            return EventReflectionTemplate(
                event=Event.objects.get(pk=self.kwargs["id"])
            )


# 直後反省の入力ページをつくる
