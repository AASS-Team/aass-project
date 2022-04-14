from django.urls import include, path

from . import views

urlpatterns = [
    path(
        "administration/tools/",
        include(
            [
                path("", views.ToolList.as_view(), name="tool-list"),
                path("new", views.ToolCreate.as_view(), name="tool-new"),
                path("<uuid:id>", views.ToolDetail.as_view(), name="tool-detail"),
                path("<uuid:id>/edit", views.ToolEdit.as_view(), name="tool-edit"),
            ]
        ),
    ),
]
