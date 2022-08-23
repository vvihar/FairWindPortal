"""ウィジェット"""
from django import template

register = template.Library()


@register.filter("startswith")
def startswith(text, starts):
    """テキストが指定された文字列で始まるかどうかを判定する"""
    if isinstance(text, str):
        return text.startswith(starts)
    return False
