from django.urls import include, path

from . import views

urlpatterns = [
    path(
        "labs/",
        include(
            [
                path("", views.LabsList.as_view(), name="lab-list"),
                path("new", views.LabCreate.as_view(), name="lab-new"),
                path("<uuid:id>", views.LabDetail.as_view(), name="lab-detail"),
                path("<uuid:id>/edit", views.LabEdit.as_view(), name="lab-edit"),
            ]
        ),
    ),
]
