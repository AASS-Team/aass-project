from django_components import component


def dict2attribute(dict):
    return "".join([f'{key}="{value}"' for key, value in dict.items()])


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


@component.register("ui-search")
class UiSearch(component.Component):
    def get_template_name(self, context):
        return "components/ui/search.html"

    def get_context_data(self, additional_classes, **kwargs):
        return {
            "additional_classes": additional_classes,
            "bruh": kwargs,
            "attributes": dict2attribute(kwargs),
        }


@component.register("ui-button")
class UiButton(component.Component):
    def get_template_name(self, context):
        return "components/ui/button.html"

    def get_context_data(
        self,
        text,
        additional_classes,
        icon,
        type,
        href,
        disabled=None,
        primary=None,
        secondary=None,
        danger=None,
        **kwargs,
    ):

        class_object = "flex justify-center items-center px-3 py-1 focus:outline-none "

        if disabled is not None and disabled is True:
            class_object += (
                "bg-gray-400 text-white hover:bg-gray-400 hover:cursor-default "
            )
        else:
            class_object += "hover:cursor-pointer "

        if primary is not None:
            class_object += "bg-yellow-500 text-white hover:bg-yellow-400 "

        if secondary is not None:
            class_object += "border border-gray-600 text-gray-600 bg-gray-200 "

        if danger is not None:
            class_object += (
                "border border-red-500 text-red-500 hover:bg-red-500 hover:text-white "
            )

        if additional_classes is not None:
            class_object += additional_classes

        return {
            "text": text,
            "icon": icon,
            "type": type,
            "href": href,
            "class_object": class_object,
            "attributes": dict2attribute(kwargs),
        }


@component.register("ui-table")
class UiTable(component.Component):
    def get_template_name(self, context):
        return "components/ui/table.html"

    def get_context_data(
        self,
        options,
    ):
        return {
            "options": options,
        }
