from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.views.generic.edit import ModelFormMixin

from events.models import Event

from .models import EventReflection

# Create your views here.


class EventReflectionList(ModelFormMixin, ListView):
    model = EventReflection
    template_name = "reflections/list.html"
    fields = ["reflection"]
    success_url = reverse_lazy("events:")

    def get_queryset(self):
        return EventReflection.objects.filter(event=self.kwargs["id"]).order_by("user")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["event"] = Event.objects.get(pk=self.kwargs["id"])
        return context

    def form_valid(self, form):
        # FIXME: 更新時にエラーが出ないようにする
        # get existing or create new
        reflection = EventReflection.objects.get_or_create(
            event=self.kwargs["id"], user=self.request.user
        )[0]
        reflection.reflection = form.cleaned_data["reflection"]
        reflection.save()
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["reflection"].initial = (
            EventReflection.objects.filter(
                event=self.kwargs["id"], user=self.request.user
            )
            .first()
            .reflection
        )
        return form

    def get(self, request, *args, **kwargs):
        self.object = None
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        self.object_list = self.get_queryset()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
