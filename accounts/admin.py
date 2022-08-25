from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models import Division, Group

# Register your models here.


class CustomUserAdmin(UserAdmin):
    """カスタムユーザーモデルの管理画面での表示をカスタマイズ"""

    # 編集時に表示するフィールド
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            "個人情報",
            {
                "fields": (
                    "last_name",
                    "first_name",
                    "email",
                    "sex",
                )
            },
        ),
        (
            "大学",
            {
                "fields": (
                    "enrolled_year",
                    "course",
                    "faculty",
                    "department",
                )
            },
        ),
        (
            "FairWind",
            {
                "fields": (
                    "grade",
                    "group",
                    "division",
                )
            },
        ),
        ("ログ", {"fields": ("last_login", "date_joined")}),
    )
    # 新規作成時に表示するフィールド
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "last_name",
                    "first_name",
                    "email",
                    "password1",
                    "password2",
                    "sex",
                    "enrolled_year",
                    "course",
                    "grade",
                ),
            },
        ),
    )
    # 一覧にしたときに表示するフィールド
    list_display = ("full_name", "grade", "course", "faculty", "group", "division")

    def full_name(self, obj):
        "フルネームを返す"
        return obj.last_name + " " + obj.first_name

    full_name.short_description = "氏名"

    list_filter = ("is_superuser", "is_staff", "is_active", "group", "division")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("grade", "username")  # 並び順を指定


CustomUser = get_user_model()
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Division)
admin.site.register(Group)

admin.site.site_header = "FairWind Portal Admin"
