from django import template

register = template.Library()


@register.simple_tag
def obj_get(obj, key, default=""):
    return obj.get(key, default)
