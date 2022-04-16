from django import template

register = template.Library()


@register.filter()
def replace(string, replace):
    replace = replace.split(",")
    return string.replace(replace[0], replace[1])
