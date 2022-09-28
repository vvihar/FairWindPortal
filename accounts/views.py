"""Accountsのビューを管理する"""
import csv
import io
from datetime import datetime

# Create your views here.
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    FormView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import CSVUploadForm, UserCreateForm, UserUpdateForm
from .models import Division, Group, User


class StaffRequiredMixin(UserPassesTestMixin):
    """管理者のみがアクセスできるビューを作成する"""

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        return redirect(f"{reverse(settings.LOGIN_URL)}?next={self.request.path}")


class Home(LoginRequiredMixin, TemplateView):
    """ホーム画面"""

    template_name = "accounts/index.html"

    def get(self, request, *args, **kwargs):
        """GETリクエスト時の処理"""
        senior_division_year = datetime.today().year - 2
        if (
            not request.user.faculty
            and request.user.enrolled_year <= senior_division_year
        ):
            messages.warning(request, "後期課程の進学先の情報を登録してください。")
        if not request.user.group:
            messages.warning(request, "所属している班の情報を登録してください。")
        if not request.user.division:
            messages.warning(request, "所属している担当の情報を登録してください。")
        return render(request, self.template_name)


class UserSignUp(StaffRequiredMixin, CreateView):
    """ユーザー登録画面"""

    model = User
    form_class = UserCreateForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("accounts:")

    def form_valid(self, form):
        """フォームが有効な場合の処理"""
        messages.success(self.request, "ユーザーを登録しました。")
        return super().form_valid(form)


class Login(LoginView):
    """ログイン画面"""

    template_name = "accounts/login.html"


class PasswordChange(PasswordChangeView):
    """パスワード変更画面"""

    template_name = "accounts/password_change.html"
    success_url = reverse_lazy("accounts:")

    def form_valid(self, form):
        """フォームが有効な場合の処理"""
        messages.success(self.request, "パスワードを変更しました。")
        return super().form_valid(form)


class UserUpdate(LoginRequiredMixin, UpdateView):
    """ユーザー編集画面"""

    model = User
    form_class = UserUpdateForm
    template_name = "accounts/update.html"
    success_url = reverse_lazy("accounts:")

    def get_object(self, queryset=None):
        """現在ログインしているユーザーのデータを取得する"""
        return self.request.user

    def form_valid(self, form):
        """フォームが有効な場合の処理"""
        messages.success(self.request, "ユーザーを更新しました。")
        return super().form_valid(form)


class GroupList(StaffRequiredMixin, ListView):
    """班一覧"""

    template_name = "accounts/group/list.html"
    model = Group


class GroupCreate(StaffRequiredMixin, CreateView):
    """班登録"""

    template_name = "accounts/group/create.html"
    model = Group
    fields = ("name",)
    success_url = reverse_lazy("accounts:group")

    def form_valid(self, form):
        messages.success(self.request, form.cleaned_data["name"] + "を登録しました。")
        return super().form_valid(form)


class GroupDelete(StaffRequiredMixin, DeleteView):
    """班削除"""

    template_name = "accounts/group/delete.html"
    model = Group
    success_url = reverse_lazy("accounts:group")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "班を削除しました。")
        return super().delete(request, *args, **kwargs)


class GroupUpdate(StaffRequiredMixin, UpdateView):
    """班編集"""

    template_name = "accounts/group/update.html"
    model = Group
    fields = ("name",)
    success_url = reverse_lazy("accounts:group")

    def form_valid(self, form):
        messages.success(self.request, form.cleaned_data["name"] + "を編集しました。")
        return super().form_valid(form)


class DivisionList(StaffRequiredMixin, ListView):
    """担当一覧"""

    template_name = "accounts/division/list.html"
    model = Division


class DivisionCreate(StaffRequiredMixin, CreateView):
    """担当登録"""

    template_name = "accounts/division/create.html"
    model = Division
    fields = ("name",)
    success_url = reverse_lazy("accounts:division")

    def form_valid(self, form):
        messages.success(self.request, form.cleaned_data["name"] + "を登録しました。")
        return super().form_valid(form)


class DivisionDelete(StaffRequiredMixin, DeleteView):
    """担当削除"""

    template_name = "accounts/division/delete.html"
    model = Division
    success_url = reverse_lazy("accounts:division")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "担当を削除しました。")
        return super().delete(request, *args, **kwargs)


class DivisionUpdate(StaffRequiredMixin, UpdateView):
    """担当編集"""

    template_name = "accounts/division/update.html"
    model = Division
    fields = ("name",)
    success_url = reverse_lazy("accounts:division")

    def form_valid(self, form):
        messages.success(self.request, form.cleaned_data["name"] + "を編集しました。")
        return super().form_valid(form)


class UserList(StaffRequiredMixin, ListView):
    """ユーザー一覧"""

    template_name = "accounts/user/list.html"
    model = User


class UserImport(StaffRequiredMixin, FormView):
    """ユーザー一括登録"""

    template_name = "accounts/user/import.html"
    form_class = CSVUploadForm
    success_url = reverse_lazy("accounts:users")

    def form_valid(self, form):
        errors = []
        new_users = []
        imported_users = 0
        # csv.readerに渡すため、TextIOWrapperでテキストモードなファイルに変換
        csvfile = io.TextIOWrapper(form.cleaned_data["file"], encoding="utf-8")
        reader = csv.reader(csvfile)
        username_list = list(User.objects.values_list("username", flat=True))
        email_list = list(User.objects.values_list("email", flat=True))
        # 1行ずつ取り出し、作成していく
        for row in reader:
            for element in row:
                element = element.strip()
            user_data = {
                "username": row[0],
                "last_name": row[1],  # 姓
                "first_name": row[2],  # 名
                "email": row[3],
                "course": row[4],
                "enrolled_year": row[5],
                "grade": row[6],
                "sex": row[7],
                "group": row[8],  # 班
                "division": row[9],  # 担当
                "password": row[10],
            }
            if user_data["username"] == "":
                messages.error(self.request, "ユーザー名が空白の行が見つかりました。")
                continue
            error_count = 0
            for key, value in user_data.items():
                if value == "" and key != "group" and key != "division":  # 担当、班は空白でも OK
                    error_temp = (
                        user_data["username"] + " は、データに空白の項目が見つかったため、読み込まれませんでした。"
                    )
                    if not error_temp in errors:
                        messages.error(self.request, error_temp)
                    error_count += 1
            if error_count > 0:
                continue
            if user_data["username"] in username_list:
                messages.error(
                    self.request,
                    user_data["username"] + " は、ユーザー名が他のユーザーと重複しているため、読み込まれませんでした。",
                )
                continue
            if user_data["email"] in email_list:
                messages.error(
                    self.request,
                    user_data["username"] + " は、メールアドレスが他のユーザーと重複しているため、読み込まれませんでした。",
                )
                continue
            if user_data["group"] != "" and not user_data["group"] in list(
                Group.objects.values_list("name", flat=True)
            ):
                messages.error(
                    self.request, user_data["username"] + " は、班が存在しないため、読み込まれませんでした。"
                )
                continue
            if user_data["division"] != "" and not user_data["division"] in list(
                Division.objects.values_list("name", flat=True)
            ):
                messages.error(
                    self.request, user_data["username"] + " は、担当が存在しないため、読み込まれませんでした。"
                )
                continue
            new_user = User(
                username=user_data["username"],
                last_name=user_data["last_name"],
                first_name=user_data["first_name"],
                email=user_data["email"],
                is_staff=False,
                is_active=True,
                is_superuser=False,
                course=user_data["course"],
                enrolled_year=user_data["enrolled_year"],
                grade=user_data["grade"],
                sex=user_data["sex"],
            )  # 一旦 User モデルを作成
            new_user.set_password(user_data["password"])  # パスワードをセット
            if user_data["group"] != "":
                new_user.group = Group.objects.get(name=user_data["group"])
            if user_data["division"] != "":
                new_user.division = Division.objects.get(name=user_data["division"])
            new_users.append(new_user)  # User モデルを保存するためのリストに追加
            imported_users += 1
        User.objects.bulk_create(new_users)  # User モデルをまとめて保存
        if imported_users > 0:
            messages.success(self.request, str(imported_users) + " 件のユーザーを読み込みました。")
        return super().form_valid(form)


@login_required
def api_members_get(request):
    """サジェスト候補のメンバーを JSON で返す。"""
    keyword = request.GET.get("keyword")
    if keyword:
        member_list = [
            {"pk": user.pk, "name": str(user.last_name + " " + user.first_name)}
            for user in User.objects.filter(
                (
                    Q(username__icontains=keyword)
                    | Q(last_name__icontains=keyword)
                    | Q(first_name__icontains=keyword)
                ),
                Q(is_active=True),
            ).all()
        ]
    else:
        member_list = []
    return JsonResponse({"object_list": member_list})
