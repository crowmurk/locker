import json
import datetime

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def pretty_json(value):
    """Форматирует объект json в виде
    удобном для восприятия
    """
    value = json.loads(value)
    return json.dumps(value, indent=4)

@register.filter
def duration(value):
    if isinstance(value, datetime.timedelta):
        seconds = int(value.total_seconds())
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60

        return '{:d}:{:02d}'.format(hours, minutes)

    return value
