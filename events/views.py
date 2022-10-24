import csv
import io
import re
from urllib import request

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, FormView, ListView, UpdateView

from .forms import EventCreateForm, MakeSchoolDBForm
from .models import Event, School

# Create your views here.


class Home(ListView):
    """ホーム画面"""

    model = Event
    template_name = "events/index.html"


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


class SchoolDetail(DetailView):
    """学校詳細"""

    model = School
    template_name = "events/school/detail.html"


class MakeSchoolDB(FormView):
    """学校データベースのDBを作成・更新する"""

    template_name = "events/school/db_update.html"
    form_class = MakeSchoolDBForm
    success_url = reverse_lazy("events:school_list")

    def form_valid(self, form):
        """フォームが有効な場合"""

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
                messages.error(self.request, "ファイルのエンコードが不正です。")
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

        School.objects.all().delete()
        School.objects.bulk_create(schools)
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


class EventUpdate(UpdateView):
    """企画更新"""

    template_name = "events/update.html"
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
        messages.success(self.request, "企画を更新しました")
        return super().form_valid(form)


class EventDetail(DetailView):
    """企画詳細"""

    template_name = "events/detail.html"
    model = Event


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
