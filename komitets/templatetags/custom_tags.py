from django import template

register = template.Library()


@register.filter
def voted_by(value, user):
    return value.voted_by(user)


@register.filter
def have_user(value, user):
    if value.filter(user=user):
        return True
    return False


@register.filter
def have_option(value, option):
    if value.filter(answer_option=option):
        return True
    return False
