from django import template

register = template.Library()


@register.filter()
def has_permission(user, permission):
    return (
        user.is_superuser or user.user_permissions.filter(codename=permission).exists()
    )
