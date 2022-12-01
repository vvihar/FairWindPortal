import markdown
from django import template

register = template.Library()


@register.filter
def md_to_html(text):
    html = markdown.markdown(
        text,
        extensions=[
            "nl2br",
            "fenced_code",
            "codehilite",
            "tables",
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
        },
    )
    html = html.replace("<table", '<table class="table"')
    return html
