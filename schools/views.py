import csv
import io
import re
from urllib import request

from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView, FormView, ListView, UpdateView

from accounts.views import StaffRequiredMixin

from .forms import MakeSchoolDBForm, SchoolDetailUpdateForm
from .models import School

# Create your views here.


class SchoolList(ListView):
    """学校一覧"""

    model = School
    template_name = "schools/list.html"
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
    template_name = "schools/detail.html"
    form_class = SchoolDetailUpdateForm


class SchoolDetailUpdate(UpdateView):
    """学校詳細の編集画面。学校に関するデータを蓄積する"""

    model = School
    template_name = "schools/detail_update.html"
    form_class = SchoolDetailUpdateForm

    def get_success_url(self):
        return reverse_lazy("schools:school_detail", kwargs={"pk": self.kwargs["pk"]})


class MakeSchoolDB(StaffRequiredMixin, FormView):
    """学校データベースのDBを作成・更新する"""

    template_name = "schools/db_update.html"
    form_class = MakeSchoolDBForm
    success_url = reverse_lazy("schools:")

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

        school_types = {
            "C1": "中学校",
            "C2": "義務教育学校",
            "D1": "高等学校",
            "D2": "中等教育学校",
        }
        establisher_types = {
            "1": "国立",
            "2": "公立",
            "3": "私立",
        }
        prefectures = {
            "01": "北海道",
            "02": "青森県",
            "03": "岩手県",
            "04": "宮城県",
            "05": "秋田県",
            "06": "山形県",
            "07": "福島県",
            "08": "茨城県",
            "09": "栃木県",
            "10": "群馬県",
            "11": "埼玉県",
            "12": "千葉県",
            "13": "東京都",
            "14": "神奈川県",
            "15": "新潟県",
            "16": "富山県",
            "17": "石川県",
            "18": "福井県",
            "19": "山梨県",
            "20": "長野県",
            "21": "岐阜県",
            "22": "静岡県",
            "23": "愛知県",
            "24": "三重県",
            "25": "滋賀県",
            "26": "京都府",
            "27": "大阪府",
            "28": "兵庫県",
            "29": "奈良県",
            "30": "和歌山県",
            "31": "鳥取県",
            "32": "島根県",
            "33": "岡山県",
            "34": "広島県",
            "35": "山口県",
            "36": "徳島県",
            "37": "香川県",
            "38": "愛媛県",
            "39": "高知県",
            "40": "福岡県",
            "41": "佐賀県",
            "42": "長崎県",
            "43": "熊本県",
            "44": "大分県",
            "45": "宮崎県",
            "46": "鹿児島県",
            "47": "沖縄県",
        }

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
            for row in reader:
                if not re.fullmatch(r"[A-H]\d{12}", row[0]):
                    continue
                for col in row:
                    if "(" in col:
                        row[row.index(col)] = col.split("(")[0]
                if (
                    not row[0]
                    or row[4] == "9"  # 本分校が9は廃校
                    or not row[1] in valid_school_type_code  # 学校種
                ):
                    continue
                # コードから文字情報に変換
                row[1] = school_types[row[1]]  # 学校種
                row[2] = prefectures[row[2]]  # 都道府県
                row[3] = establisher_types[row[3]]  # 設置区分

                if row[0] in existing_schoolcodes:  # 学校コード
                    school = existing_schools[
                        existing_schoolcodes.index(row[0])  # 学校コード
                    ]
                    school.type = row[1]  # 学校種
                    school.prefecture = row[2]  # 都道府県
                    school.establisher = row[3]  # 設置区分
                    school.name = row[5]  # 学校名
                    school.number = number  # 通し番号
                else:
                    school = School(
                        code=row[0],  # 学校コード
                        type=row[1],  # 学校種
                        prefecture=row[2],  # 都道府県
                        establisher=row[3],  # 設置区分
                        name=row[5],  # 学校名
                        number=number,  # 通し番号
                    )
                    schools.append(school)

                number += 1

        School.objects.bulk_create(schools)
        School.objects.bulk_update(
            existing_schools, ["type", "prefecture", "establisher", "name", "number"]
        )
        messages.success(self.request, "学校データを更新しました")
        return super().form_valid(form)


def api_schools_get(request):
    """サジェスト候補の学校を JSON で返す。"""
    keyword = request.GET.get("keyword")
    if keyword:
        keyword = keyword.replace("高校", "高等学校")
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
