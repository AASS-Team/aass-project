from django import template

register = template.Library()


@register.filter()
def boolean(var):
    return bool(var)


@register.filter()
def negate(var):
    return not var
