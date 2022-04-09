from django import template

register = template.Library()


@register.simple_tag
def get_table_row_class(options, index, misc=True):
    class_object = ""

    if misc is True:
        class_object += "py-3 border-b border-gray-200 "

    try:
        row_layout = options["layout"][index]
    except IndexError:
        return class_object

    if "width" in row_layout and row_layout["width"] is not None:
        class_object += f"w-{options['layout'][index]['width']} "

    if "width-sm" in row_layout and row_layout["width-sm"] is not None:
        class_object += f"sm:w-{options['layout'][index]['width-sm']} "

    if "left" in row_layout and row_layout["left"] is not None:
        class_object += "first:pl-6 text-left justify-start"

    return class_object
