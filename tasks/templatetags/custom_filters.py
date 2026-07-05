from django import template
import calendar

register = template.Library()

@register.filter
def get_month_name(month_number):
    try:
        return calendar.month_name[int(month_number)]
    except (ValueError, IndexError):
        return ""