from django import template

register = template.Library()


@register.simple_tag()
def concat_url(*args):
    return "/".join(map(lambda x: str(x).strip("/"), args))
