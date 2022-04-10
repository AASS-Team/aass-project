from django import template

register = template.Library()


@register.simple_tag
def get_current_url(request):
    return request.build_absolute_uri(request.path)
