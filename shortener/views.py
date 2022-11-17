import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import BadRequest
from django.core.validators import URLValidator
from django.http import Http404
from django.shortcuts import redirect
from django.utils.timezone import make_aware
from django.views import View
from django.views.generic.edit import FormMixin

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


def make_short_url(request):
    """短縮URLを作成する"""
    check_expire_date()
    if request.method == "POST":
        redirect_to = request.POST["redirect_to"]
        if ShortURL.objects.filter(redirect_to=redirect_to).exists():
            shorturl = ShortURL.objects.get(redirect_to=redirect_to)
            shorturl.created_at = make_aware(datetime.datetime.now())
            shorturl.save()
        else:
            shorturl = ShortURL(redirect_to=redirect_to)
            shorturl.save()
        hashid = shorturl.hashid
        previous_url = request.META.get("HTTP_REFERER", "/")
        # add hashid to previous_url as a query parameter
        if "?" in previous_url:
            # if any query parameters already exist, add hashid to the end with &
            success_url = f"{previous_url}&hashid={hashid}"
        else:
            success_url = f"{previous_url}?hashid={hashid}"
        messages.success(request, f"短縮URLを生成しました")
        return redirect(success_url)
    else:
        raise Http404("Invalid request")


class MakeShortURL(LoginRequiredMixin, FormMixin, View):
    """短縮URLを作成する。GETリクエストは受け付けない"""

    fields = ["redirect_to"]
    template_name = "shortener/shortener.html"  # 消す

    def get_success_url(self):
        # return to the previous page
        return self.request.META.get("HTTP_REFERER", "/")

    def post(self, request, *args, **kwargs):
        check_expire_date()
        redirect_to = request.POST["redirect_to"]
        if ShortURL.objects.filter(redirect_to=redirect_to).exists():
            return self.form_invalid(self.get_form())
        return self.form_valid(self.get_form())

    def form_invalid(self, form):
        # return existing shorturl if exists
        redirect_to = self.request.POST["redirect_to"]
        if ShortURL.objects.filter(redirect_to=redirect_to).exists():
            shorturl = ShortURL.objects.get(redirect_to=redirect_to)
            messages.info(self.request, f"短縮URLを作成しました：{shorturl}")
            return super().form_valid(form)
        return super().form_invalid(form)

    def form_valid(self, form):
        scheme = self.request.scheme
        host = self.request.get_host()
        form.save()
        hashid = form.instance.hashid
        shorturl = f"{scheme}://{host}/s/{hashid}"
        messages.success(self.request, f"短縮URLを作成しました：{shorturl}")
        return super().form_valid(form)

    """
    def get(self, request, *args, **kwargs):
        raise BadRequest("GET method is not allowed")
    """


def redirect_to(request, hashid):
    """正規のURLにリダイレクトする"""
    check_expire_date()
    try:
        shorturl = ShortURL.objects.get(hashid=hashid)
    except ShortURL.DoesNotExist:
        raise Http404("Invalid short URL")
    return redirect(shorturl.redirect_to)
