from django import template

register = template.Library()

@register.filter
def divide(value, arg):
    try:
        return round((int(value) / int(arg)) * 100, 1)
    except (ValueError, ZeroDivisionError):
        return None