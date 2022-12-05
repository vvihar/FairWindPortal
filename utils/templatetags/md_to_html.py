import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def md_to_html(text):
    html = markdown.markdown(
        text,
        extensions=[
            "extra",
            "nl2br",
            "fenced_code",
            "codehilite",
            "toc",
            "sane_lists",
            "smarty",
            "wikilinks",
            "markdown_link_attr_modifier",
        ],
        extension_configs={
            "markdown_link_attr_modifier": {
                "new_tab": "on",
                "no_referrer": "external_only",
            },
            "codehilite": {
                "pygments_style": "monokai",
                "noclasses": True,
            },
        },
    )
    html = html.replace("<table", '<table class="table"')
    return mark_safe(html)