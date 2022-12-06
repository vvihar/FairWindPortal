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
            "attr_list",
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

    reflection_list = (
        (
            "[o]",
            "<span class='badge bg-success rounded-pill me-1' style='width:2.5rem'>○</span>",
        ),
        (
            "[x]",
            "<span class='badge bg-danger rounded-pill me-1' style='width:2.5rem'>×</span>",
        ),
        (
            "[/]",
            "<span class='badge bg-warning text-dark rounded-pill me-1' style='width:2.5rem'>△</span>",
        ),
    )
    for before, after in reflection_list:
        html = html.replace(before, after)
    return mark_safe(html)
