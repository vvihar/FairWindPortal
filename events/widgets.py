"""Eventsのウィジェットを管理"""

from django import forms, template
from django.forms import widgets


class SplitDateTimeWidget(widgets.SplitDateTimeWidget):
    """SplitDateTimeWidgetのカスタマイズ"""

    template_name = "widgets/splitdatetime.html"

    def decompress(self, value):
        if value:
            return [value.start, value.stop]
        return [None, None]

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        date_widget = context["widget"]["subwidgets"][0]
        time_widget = context["widget"]["subwidgets"][1]
        date_widget["type"] = "date"
        time_widget["type"] = "time"
        context["widget"]["date"] = date_widget
        context["widget"]["time"] = time_widget
        return context
