from django import template

register = template.Library()


@register.filter()
def has_group(user, group_list_or_group_name):
    return user.is_superuser or (
        user.groups.filter(name__in=group_list_or_group_name).exists()
        if isinstance(group_list_or_group_name, list)
        else user.groups.filter(name=group_list_or_group_name).exists()
    )
