from django import template

register = template.Library()


@register.simple_tag
def active_route(request, route):
    return route in request.path
