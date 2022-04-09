from django_components import component


@component.register("user-circle")
class UserCircle(component.Component):
    def get_template_name(self, context):
        return "components/user-circle/user-circle.html"

    def get_context_data(self, name):
        return {
            "name": name,
        }


@component.register("navigation-group")
class NavigationGroup(component.Component):
    def get_template_name(self, context):
        return "components/navigation/navigation-group/navigation-group.html"

    def get_context_data(self, group):
        return {
            "group": group,
        }


@component.register("navigation-item")
class NavigationItem(component.Component):
    def get_template_name(self, context):
        return "components/navigation/navigation-item/navigation-item.html"

    def get_context_data(self, item):
        return {
            "item": item,
        }
