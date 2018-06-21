from django import template

register = template.Library()


@register.filter
def is_voted_by(value, arg):
    return value.is_voted_by(arg)
