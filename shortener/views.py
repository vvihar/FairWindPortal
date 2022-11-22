import datetime

from django.contrib import messages
from django.http import Http404
from django.shortcuts import redirect
from django.utils.timezone import make_aware

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


def redirect_to(request, hashid):
    """正規のURLにリダイレクトする"""
    check_expire_date()
    try:
        shorturl = ShortURL.objects.get(hashid=hashid)
    except ShortURL.DoesNotExist:
        raise Http404("Invalid short URL")
    return redirect(shorturl.redirect_to)
