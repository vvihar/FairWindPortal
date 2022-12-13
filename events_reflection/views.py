from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView
from events.models import Event
from events.views import OnlyEventAdminMixin, OnlyEventParticipantMixin

from .forms import EventReflectionForm
from .models import (
    EventReflection,
    EventReflectionGeneral,
    EventReflectionTemplate,
)

# Create your views here.


class EventReflectionList(ListView):
    template_name = "reflections/list.html"
    model = EventReflection
    form_class = EventReflectionForm

    def get_queryset(self):
        return EventReflection.objects.filter(
            event=self.kwargs["id"]
        ).order_by("user")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["event"] = Event.objects.get(pk=self.kwargs["id"])
        try:
            context["reflection_general"] = EventReflectionGeneral.objects.get(
                event=self.kwargs["id"]
            )
        except EventReflectionGeneral.DoesNotExist:
            context["reflection_general"] = None
        return context


class EventReflectionCreateUpdate(OnlyEventParticipantMixin, UpdateView):
    template_name = "reflections/edit.html"
    model = EventReflection
    form_class = EventReflectionForm

    def get_success_url(self):
        return reverse_lazy(
            "events:reflection_list", kwargs={"id": self.kwargs["id"]}
        )

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
        if not message:
            # if message is empty, delete the reflection
            event_reflection = self.get_object()
            event_reflection.delete()
            return HttpResponseRedirect(self.get_success_url())
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

    def get_object(self, queryset=None):
        try:
            return EventReflection.objects.get(
                event=self.kwargs["id"], user=self.request.user
            )
        except EventReflection.DoesNotExist:
            return EventReflection(
                event=Event.objects.get(pk=self.kwargs["id"]),
                user=self.request.user,
            )


class EventReflectionTemplateCreateUpdate(OnlyEventAdminMixin, UpdateView):
    template_name = "reflections/edit_template.html"
    model = EventReflectionTemplate
    fields = ("reflection",)

    def get_success_url(self):
        return reverse_lazy(
            "events:reflection_list", kwargs={"id": self.kwargs["id"]}
        )

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


class EventReflectionGeneralCreateUpdate(
    OnlyEventParticipantMixin, UpdateView
):
    template_name = "reflections/edit.html"
    model = EventReflectionGeneral
    fields = ("reflection",)

    def get_success_url(self):
        return reverse_lazy(
            "events:reflection_list", kwargs={"id": self.kwargs["id"]}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["event"] = Event.objects.get(pk=self.kwargs["id"])
        context["general"] = True
        return context

    def form_valid(self, form):
        message = form.cleaned_data["reflection"]
        if not message:
            # if message is empty, delete the reflection
            event_reflection = self.get_object()
            event_reflection.delete()
            return HttpResponseRedirect(self.get_success_url())
        return super().form_valid(form)

    def get_object(self, queryset=None):
        try:
            return EventReflectionGeneral.objects.get(event=self.kwargs["id"])
        except EventReflectionGeneral.DoesNotExist:
            return EventReflectionGeneral(
                event=Event.objects.get(pk=self.kwargs["id"])
            )


# 直後反省の入力ページをつくる
