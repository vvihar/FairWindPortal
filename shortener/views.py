import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import BadRequest
from django.core.validators import URLValidator
from django.http import Http404
from django.shortcuts import redirect
from django.utils.timezone import make_aware
from django.views.generic import CreateView

from .models import ShortURL

# Create your views here.


def check_expire_date():
    """短縮URLの有効期限をチェックする"""
    shorturls = ShortURL.objects.all()
    for shorturl in shorturls:
        # 有効期限は30日
        if shorturl.created_at + datetime.timedelta(days=30) < make_aware(
            datetime.datetime.now()
        ):
            shorturl.delete()


class MakeShortURL(LoginRequiredMixin, CreateView):
    """短縮URLを作成する。GETリクエストは受け付けない"""

    model = ShortURL
    success_url = "/"
    fields = ["redirect_to", "title"]

    def form_valid(self, form):
        redirect_to = form.cleaned_data["redirect_to"]
        scheme = self.request.scheme
        host = self.request.get_host()
        url = f"{scheme}://{host}{redirect_to}"
        if not URLValidator()(url):
            return super().form_invalid(form)
        form.save()
        hashid = form.instance.hashid
        shorturl = f"{scheme}://{host}/s/{hashid}"
        messages.success(self.request, f"短縮URLを作成しました：{shorturl}")
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        raise BadRequest("GET method is not allowed")

    def post(self, request, *args, **kwargs):
        check_expire_date()
        return super().post(request, *args, **kwargs)


def redirect_to(request, hashid):
    """正規のURLにリダイレクトする"""
    check_expire_date()
    try:
        shorturl = ShortURL.objects.get(hashid=hashid)
    except ShortURL.DoesNotExist:
        raise Http404("Invalid short URL")
    return redirect(shorturl.redirect_to)
