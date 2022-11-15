import csv
import io
import re
from http.client import HTTPResponse
from urllib import request

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q
from django.http import JsonResponse
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
    MakeSchoolDBForm,
    SchoolDetailUpdateForm,
)
from .models import Event, EventParticipation, School, SchoolDetail

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


class SchoolList(ListView):
    """学校一覧"""

    model = School
    template_name = "events/school/list.html"
    paginate_by = 100

    def get_queryset(self):
        q_word = self.request.GET.get("search")
        if q_word:
            q_word = q_word.replace("高校", "高等学校")
            object_list = School.objects.filter(
                Q(name__icontains=q_word)
                | Q(prefecture__icontains=q_word)
                | Q(type__icontains=q_word)
                | Q(establisher__icontains=q_word)
                | Q(code__icontains=q_word)
            ).order_by("number")
        else:
            object_list = School.objects.all().order_by("number")
        return object_list


class SchoolDetailView(DetailView):
    """学校詳細"""

    model = School
    template_name = "events/school/detail.html"
    form_class = SchoolDetailUpdateForm


class SchoolDetailUpdate(UpdateView):
    """学校詳細の編集画面。学校に関するデータを蓄積する"""

    model = SchoolDetail
    template_name = "events/school/detail_update.html"
    form_class = SchoolDetailUpdateForm

    def get_success_url(self):
        return reverse_lazy("events:school_detail", kwargs={"pk": self.kwargs["pk"]})


class MakeSchoolDB(FormView):
    """学校データベースのDBを作成・更新する"""

    template_name = "events/school/db_update.html"
    form_class = MakeSchoolDBForm
    success_url = reverse_lazy("events:school_list")

    def form_valid(self, form):
        """フォームが有効な場合"""

        existing_schools = School.objects.all()
        existing_schoolcodes = [school.code for school in existing_schools]

        url_east = form.cleaned_data["file_url_east"]
        url_west = form.cleaned_data["file_url_west"]
        urls = [url_east, url_west]

        encoding = form.cleaned_data["encoding"]

        valid_school_type_code = ("C1", "C2", "D1", "D2")
        # C1:中学校, C2:義務教育学校, D1:高等学校, D2:中等教育学校

        schools = []

        prefectures = (
            ("01", "北海道"),
            ("02", "青森県"),
            ("03", "岩手県"),
            ("04", "宮城県"),
            ("05", "秋田県"),
            ("06", "山形県"),
            ("07", "福島県"),
            ("08", "茨城県"),
            ("09", "栃木県"),
            ("10", "群馬県"),
            ("11", "埼玉県"),
            ("12", "千葉県"),
            ("13", "東京都"),
            ("14", "神奈川県"),
            ("15", "新潟県"),
            ("16", "富山県"),
            ("17", "石川県"),
            ("18", "福井県"),
            ("19", "山梨県"),
            ("20", "長野県"),
            ("21", "岐阜県"),
            ("22", "静岡県"),
            ("23", "愛知県"),
            ("24", "三重県"),
            ("25", "滋賀県"),
            ("26", "京都府"),
            ("27", "大阪府"),
            ("28", "兵庫県"),
            ("29", "奈良県"),
            ("30", "和歌山県"),
            ("31", "鳥取県"),
            ("32", "島根県"),
            ("33", "岡山県"),
            ("34", "広島県"),
            ("35", "山口県"),
            ("36", "徳島県"),
            ("37", "香川県"),
            ("38", "愛媛県"),
            ("39", "高知県"),
            ("40", "福岡県"),
            ("41", "佐賀県"),
            ("42", "長崎県"),
            ("43", "熊本県"),
            ("44", "大分県"),
            ("45", "宮崎県"),
            ("46", "鹿児島県"),
            ("47", "沖縄県"),
        )

        number = 1

        for url in urls:
            http_response = request.urlopen(url)
            csvfile = io.TextIOWrapper(http_response, encoding=encoding)
            reader = csv.reader(csvfile)
            try:
                next(reader)
            except UnicodeDecodeError:
                messages.error(self.request, "ファイルの文字コードが不正です。")
                return super().form_invalid(form)
            for row_raw in reader:
                row = []
                for col in row_raw:
                    col = re.sub(r"\(.+?\)", "", col)
                    row.append(col)
                school_data = {
                    "学校コード": row[0],
                    "学校種": row[1],
                    "都道府県": row[2],
                    "設置区分": row[3],
                    "本分校": row[4],
                    "学校名": row[5],
                }
                if (
                    not school_data["学校コード"]
                    or school_data["本分校"] == "9"
                    or not school_data["学校種"] in valid_school_type_code
                ):
                    continue  # 本分校が9は廃校
                if school_data["学校種"] == "C1":
                    school_data["学校種"] = "中学校"
                elif school_data["学校種"] == "C2":
                    school_data["学校種"] = "義務教育学校"
                elif school_data["学校種"] == "D1":
                    school_data["学校種"] = "高等学校"
                elif school_data["学校種"] == "D2":
                    school_data["学校種"] = "中等教育学校"

                if school_data["設置区分"] == "1":
                    school_data["設置区分"] = "国立"
                elif school_data["設置区分"] == "2":
                    school_data["設置区分"] = "公立"
                elif school_data["設置区分"] == "3":
                    school_data["設置区分"] = "私立"

                if school_data["本分校"] == "1":
                    school_data["本分校"] = "本校"
                elif school_data["本分校"] == "2":
                    school_data["本分校"] = "分校"

                for prefecture in prefectures:
                    if school_data["都道府県"] == prefecture[0]:
                        school_data["都道府県"] = prefecture[1]
                        break

                if school_data["学校コード"] in existing_schoolcodes:
                    school = existing_schools[
                        existing_schoolcodes.index(school_data["学校コード"])
                    ]
                    school.type = school_data["学校種"]
                    school.prefecture = school_data["都道府県"]
                    school.establisher = school_data["設置区分"]
                    school.name = school_data["学校名"]
                    school.number = number
                else:
                    school = School(
                        code=school_data["学校コード"],
                        type=school_data["学校種"],
                        prefecture=school_data["都道府県"],
                        establisher=school_data["設置区分"],
                        name=school_data["学校名"],
                        number=number,
                    )
                    schools.append(school)

                number += 1

        School.objects.bulk_create(schools)
        School.objects.bulk_update(
            existing_schools, ["type", "prefecture", "establisher", "name", "number"]
        )
        messages.success(self.request, "学校データを更新しました")
        return super().form_valid(form)


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


class EventReplyInvitation(OnlyInvitedMixin, UpdateView):
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


def redirect_my_invitation(request, pk):
    """自分に打診された企画の打診回答ページにリダイレクトする"""
    try:
        participation = EventParticipation.objects.get(
            participant=request.user, event=pk
        )
        return redirect("events:event_reply_invitation", pk=participation.pk, id=pk)
    except EventParticipation.DoesNotExist:
        messages.error(request, "この企画には打診されていません")
        return redirect("events:event_detail", pk=pk)


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


@login_required
def api_schools_get(request):
    """サジェスト候補の学校を JSON で返す。"""
    keyword = request.GET.get("keyword")
    keyword = keyword.replace("高校", "高等学校")
    if keyword:
        school_list = [
            {"pk": school.pk, "name": f"{school.name}（{school.prefecture}）"}
            for school in School.objects.filter(
                Q(name__icontains=keyword)
                | Q(prefecture__icontains=keyword)
                | Q(type__icontains=keyword)
                | Q(establisher__icontains=keyword)
            ).all()
        ]
    else:
        school_list = []
    return JsonResponse({"object_list": school_list})
