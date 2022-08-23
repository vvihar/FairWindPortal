"""ルートのビューを管理"""
from django.views.generic import TemplateView


class Home(TemplateView):
    """トップページ"""

    template_name = "index.html"
