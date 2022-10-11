from accounts.models import Group, User
from django.db import models

# Create your models here.


class School(models.Model):
    code = models.CharField(max_length=13, primary_key=True, verbose_name="学校コード")

    number = models.IntegerField(verbose_name="管理用連番", default=0)

    TYPE_CHOICES = (
        ("中学校", "中学校"),
        ("義務教育学校", "義務教育学校"),
        ("高等学校", "高等学校"),
        ("中等教育学校", "中等教育学校"),
    )
    type = models.CharField(max_length=6, choices=TYPE_CHOICES, verbose_name="学校種")

    PREFECTURE_CHOICE = (
        ("北海道", "北海道"),
        ("青森県", "青森県"),
        ("岩手県", "岩手県"),
        ("宮城県", "宮城県"),
        ("秋田県", "秋田県"),
        ("山形県", "山形県"),
        ("福島県", "福島県"),
        ("茨城県", "茨城県"),
        ("栃木県", "栃木県"),
        ("群馬県", "群馬県"),
        ("埼玉県", "埼玉県"),
        ("千葉県", "千葉県"),
        ("東京都", "東京都"),
        ("神奈川県", "神奈川県"),
        ("新潟県", "新潟県"),
        ("富山県", "富山県"),
        ("石川県", "石川県"),
        ("福井県", "福井県"),
        ("山梨県", "山梨県"),
        ("長野県", "長野県"),
        ("岐阜県", "岐阜県"),
        ("静岡県", "静岡県"),
        ("愛知県", "愛知県"),
        ("三重県", "三重県"),
        ("滋賀県", "滋賀県"),
        ("京都府", "京都府"),
        ("大阪府", "大阪府"),
        ("兵庫県", "兵庫県"),
        ("奈良県", "奈良県"),
        ("和歌山県", "和歌山県"),
        ("鳥取県", "鳥取県"),
        ("島根県", "島根県"),
        ("岡山県", "岡山県"),
        ("広島県", "広島県"),
        ("山口県", "山口県"),
        ("徳島県", "徳島県"),
        ("香川県", "香川県"),
        ("愛媛県", "愛媛県"),
        ("高知県", "高知県"),
        ("福岡県", "福岡県"),
        ("佐賀県", "佐賀県"),
        ("長崎県", "長崎県"),
        ("熊本県", "熊本県"),
        ("大分県", "大分県"),
        ("宮崎県", "宮崎県"),
        ("鹿児島県", "鹿児島県"),
        ("沖縄県", "沖縄県"),
    )
    prefecture = models.CharField(
        max_length=4, choices=PREFECTURE_CHOICE, verbose_name="都道府県"
    )

    ESTABLISHER_CHOICE = (
        ("国立", "国立"),
        ("公立", "公立"),
        ("私立", "私立"),
    )
    establisher = models.CharField(
        max_length=2, choices=ESTABLISHER_CHOICE, default="公立", verbose_name="設置区分"
    )

    name = models.CharField(max_length=50, verbose_name="学校名")

    # TODO: 企画と many to many

    class Meta:
        """メタ情報"""

        verbose_name = "学校"
        verbose_name_plural = "学校"

    def __str__(self):
        return self.name


class SchoolDetail(models.Model):
    school = models.OneToOneField(
        School,
        on_delete=models.DO_NOTHING,
        verbose_name="学校",
        related_name="detail",
        primary_key=True,
        db_constraint=False,
    )

    memo = models.TextField(verbose_name="備考", blank=True, null=True)
    # TODO: Markdown を導入する
    # TODO: 新規作成＆編集画面を実装する

    class Meta:
        """メタ情報"""

        verbose_name = "学校詳細"
        verbose_name_plural = "学校詳細"

    def __str__(self):
        return f"{self.school.prefecture} {self.school.name}"


class Event(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="企画名",
        unique=True,
        blank=True,
        null=True,
        default=None,
        help_text="空欄の場合は、対象校名と種別を組み合わせて表示します",
    )

    TYPE_CHOICES = (
        ("オンライン", "オンライン"),
        ("ハイブリッド", "ハイブリッド"),
        ("出張", "出張"),
        ("ツアー", "ツアー"),
    )

    type = models.CharField(
        verbose_name="種別",
        max_length=6,
        choices=TYPE_CHOICES,
    )

    start_datetime = models.DateTimeField(verbose_name="開始日時")
    end_datetime = models.DateTimeField(verbose_name="終了日時")

    person_in_charge = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        verbose_name="統括",
        null=True,
        related_name="event_in_charge",
    )

    admin = models.ManyToManyField(
        User, verbose_name="管理者", related_name="event_admin", blank=True
    )

    participants = models.ManyToManyField(
        User, verbose_name="参加者", related_name="event_participate_in"
    )

    school = models.ManyToManyField(School, verbose_name="対象校", related_name="event")

    group_in_charge = models.ForeignKey(
        Group, on_delete=models.SET_NULL, verbose_name="担当班", null=True, blank=True
    )

    class Meta:
        verbose_name = "イベント"
        verbose_name_plural = "イベント"

    def __str__(self):
        if self.name:
            return self.name
        else:
            event_name = ""
            for school in self.school.all():
                event_name += school.name + " "
            return f"{event_name}{self.type}"
