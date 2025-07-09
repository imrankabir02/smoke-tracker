from django import template

register = template.Library()

@register.filter(name='add')
def add(value, arg):
    """Adds the arg to the value."""
    try:
        return int(value) + int(arg)
    except (ValueError, TypeError):
        try:
            return value + arg
        except Exception:
            return ''
