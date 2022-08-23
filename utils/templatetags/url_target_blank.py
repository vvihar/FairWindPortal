"""ウィジェット"""
from django import template

register = template.Library()


def url_target_blank(text):
    """ハイパーリンクを新しいタブで開く"""
    return text.replace("<a ", '<a target="_blank" ')


url_target_blank = register.filter(url_target_blank, is_safe=True)
