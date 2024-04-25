from django import template

register = template.Library()

@register.filter
def cycle_list(value, arg):
    return value[arg % len(value)]