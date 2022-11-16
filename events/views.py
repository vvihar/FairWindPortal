from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    UpdateView,
    edit,
)

from .forms import (
    EventCreateForm,
    EventMakeInvitationForm,
    EventReplyInvitationForm,
    EventStatusUpdateForm,
)
from .models import Event, EventParticipation

# Create your views here.


class OnlyInvitedMixin(UserPassesTestMixin):
    """打診された人と管理者のみがアクセスできるMixin"""

    raise_exception = True

    def test_func(self):
        user = self.request.user
        participation = get_object_or_404(EventParticipation, pk=self.kwargs["pk"])
        if user == participation.participant:
            return True
        # FIXME: 企画の管理者用の編集ページを作る
        elif user.is_staff:
            messages.error(self.request, "打診対象者ではなく、サイトの管理者としてこのページにアクセスしています")
            return True
        else:
            return False

    def handle_no_permission(self):
        return redirect(f"{reverse(settings.LOGIN_URL)}?next={self.request.path}")


class OnlyEventAdminMixin(UserPassesTestMixin):
    """
    企画の管理者と管理者のみがアクセスできるMixin
    eventは <int:id> で指定する
    """

    raise_exception = True

    def test_func(self):
        user = self.request.user
        event = get_object_or_404(Event, pk=self.kwargs["id"])
        event_admin = event.admin.all()
        if user in event_admin:
            return True
        elif user.is_staff:
            messages.error(self.request, "企画の管理者ではなく、サイトの管理者としてこのページにアクセスしています")
            return True
        else:
            return False

    def handle_no_permission(self):
        return redirect(f"{reverse(settings.LOGIN_URL)}?next={self.request.path}")


class Home(ListView):
    """ホーム画面"""

    model = Event
    template_name = "events/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        events = Event.objects.exclude(status="アーカイブ").order_by("-start_datetime")
        for event in events:
            if self.request.user.pk in event.participation.filter(
                status="回答待ち"
            ).values_list("participant", flat=True):
                messages.info(self.request, f"{event}に打診されています")
        return context

    def get_queryset(self):
        return Event.objects.all().order_by("start_datetime")


class EventListAll(ListView):
    """全ての企画のリスト"""

    model = Event
    template_name = "events/event_list.html"

    def get_queryset(self):
        return Event.objects.all().order_by("start_datetime")


class EventCreate(CreateView):
    """企画作成"""

    template_name = "events/create.html"
    model = Event
    form_class = EventCreateForm
    success_url = reverse_lazy("events:")

    def form_valid(self, form):
        event = form.save(commit=False)
        if event.name is None:
            schools = form.cleaned_data["school"]
            school_joined = ""
            for school in schools:
                school_joined += school.name + " "
            event.name = school_joined + event.type
        event.save()
        messages.success(self.request, "企画を登録しました")
        return super().form_valid(form)


class EventUpdate(UserPassesTestMixin, UpdateView):
    """企画更新"""

    template_name = "events/update.html"
    model = Event
    form_class = EventCreateForm

    def get_success_url(self):
        return reverse_lazy("events:event_detail", kwargs={"pk": self.kwargs["pk"]})

    def form_valid(self, form):
        event = form.save(commit=False)
        if event.name is None:
            schools = form.cleaned_data["school"]
            school_joined = ""
            for school in schools:
                school_joined += school.name + " "
            event.name = school_joined + event.type
        event.save()
        messages.success(self.request, "企画を更新しました")
        return super().form_valid(form)

    def test_func(self):
        user = self.request.user
        event = self.get_object()
        if user in event.admin.all():
            return True
        elif user.is_staff:
            messages.error(self.request, "企画の管理者ではなく、サイトの管理者としてこのページにアクセスしています")
            return True
        else:
            return False

    def handle_no_permission(self):
        return redirect(f"{reverse(settings.LOGIN_URL)}?next={self.request.path}")


class EventDetail(DetailView, edit.ModelFormMixin):
    """企画詳細"""

    template_name = "events/detail.html"
    model = Event
    form_class = EventStatusUpdateForm

    def get_success_url(self):
        return reverse_lazy("events:event_detail", kwargs={"pk": self.kwargs["pk"]})

    def form_valid(self, form):
        event = form.save(commit=False)
        # 打診中の人がいないか確認する
        if (
            event.status != "参加者募集中"
            and event.status != "参加者打診中"
            and event.participation.filter(status="回答待ち").exists()
        ):
            messages.error(self.request, "打診中の人がいるため、ステータスは更新されませんでした")
            return redirect("events:event_detail", pk=self.kwargs["pk"])
        event.save()
        messages.success(self.request, f"企画のステータスを「{event.status}」に更新しました")
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get(self, request, *args, **kwargs):
        if request.user.pk in self.get_object().participation.filter(
            status="回答待ち"
        ).values_list("participant", flat=True):
            messages.info(request, "この企画に打診されています")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        participations = self.get_object().participation.filter(status="参加")
        participations_list = ""
        for participation in participations:
            participations_list += str(participation.participant) + "、"
        context["participants"] = participations_list[:-1]
        context[
            "is_invited"
        ] = self.request.user.pk in self.get_object().participation.filter(
            status="回答待ち"
        ).values_list(
            "participant", flat=True
        )
        return context


class EventParticipants(ListView):
    """企画の参加者・打診状況一覧"""

    template_name = "events/participants.html"
    model = EventParticipation

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = Event.objects.get(id=self.kwargs["pk"])
        context["object_list"] = EventParticipation.objects.filter(event=event)
        context["event"] = event
        context["counter_participate"] = len(context["object_list"].filter(status="参加"))
        context["counter_waiting"] = len(context["object_list"].filter(status="回答待ち"))
        context["is_accepting"] = event.status == "参加者募集中" or event.status == "参加者打診中"
        return context


class EventMakeInvitation(OnlyEventAdminMixin, FormView):
    """企画へ打診する"""

    template_name = "events/make_invitation.html"
    form_class = EventMakeInvitationForm

    def get_success_url(self):
        return reverse_lazy(
            "events:event_participants", kwargs={"pk": self.kwargs["id"]}
        )

    def get_context_data(self, **kwargs):
        event = get_object_or_404(Event, pk=self.kwargs["id"])
        context = super().get_context_data()
        context["event"] = event
        context["is_accepting"] = event.status == "参加者募集中" or event.status == "参加者打診中"
        return context

    def form_valid(self, form):
        if not self.get_context_data()["is_accepting"]:
            messages.error(self.request, "この企画の参加者はすでに確定しました")
            return redirect("events:event_detail", pk=self.kwargs["id"])
        participants = form.cleaned_data["participants"]
        event = get_object_or_404(Event, pk=self.kwargs["id"])
        invitations = []
        for participant in participants:
            invitation = EventParticipation(
                event=event, participant=participant, status="回答待ち"
            )
            if not participant.pk in event.participation.all().values_list(
                "participant", flat=True
            ):  # 既に打診された人には打診しない
                invitations.append(invitation)
            else:
                messages.warning(
                    self.request,
                    str(participant).replace(" ", "") + "さんは既にこの企画に打診されています",
                )
        EventParticipation.objects.bulk_create(invitations)
        return super().form_valid(form)


class EventReplyInvitation(UpdateView):
    """企画への打診を回答する"""

    template_name = "events/reply_invitation.html"
    model = EventParticipation
    form_class = EventReplyInvitationForm

    def get_success_url(self):
        return reverse_lazy(
            "events:event_participants", kwargs={"pk": self.kwargs["id"]}
        )

    def form_valid(self, form):
        status = form.cleaned_data["status"]
        messages.success(self.request, f"「{status}」で登録しました")
        return super().form_valid(form)

    def get_object(self):
        try:
            return EventParticipation.objects.get(
                participant=self.request.user, event=self.kwargs["id"]
            )
        except EventParticipation.DoesNotExist:
            messages.error(self.request, "この企画には打診されていません")
            return None

    def dispatch(self, request, *args, **kwargs):
        """打診されていない場合は企画詳細ページにリダイレクト"""
        if not self.get_object():
            return redirect("events:event_detail", pk=self.kwargs["id"])
        return super().dispatch(request, *args, **kwargs)


class EventCancelInvitation(OnlyEventAdminMixin, DeleteView):
    """企画への打診を取り消す"""

    template_name = "events/cancel_invitation.html"
    model = EventParticipation

    def get_success_url(self):
        return reverse_lazy(
            "events:event_participants", kwargs={"pk": self.kwargs["id"]}
        )

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "打診を取り消しました")
        return super().delete(request, *args, **kwargs)
