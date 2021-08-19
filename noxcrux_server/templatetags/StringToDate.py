from django import template
from datetime import datetime

register = template.Library()


@register.filter
def string_to_date(value):
    # Remove trailing "Z"
    return datetime.fromisoformat(value[:-1])
