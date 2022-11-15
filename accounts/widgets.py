"""アカウント関連のウィジェットを管理する"""
from django import forms


class SuggestWidget(forms.SelectMultiple):
    """ユーザー補完用のウィジェット"""

    template_name = "accounts/widgets/suggest.html"

    class Media:
        """Metaクラス"""

        js = ("utils/js/suggest.js",)
        css = {"all": ("utils/css/suggest.css",)}

    def __init__(self, attrs=None):
        super().__init__(attrs)
        if "class" in self.attrs:
            self.attrs["class"] += " suggest"
        else:
            self.attrs["class"] = "suggest"
