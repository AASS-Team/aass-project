from django.urls import include, path

from . import views

urlpatterns = [
    path(
        "samples/",
        include(
            [
                path("", views.SampleList.as_view(), name="sample-list"),
                path("new", views.SampleCreate.as_view(), name="sample-new"),
                path("<uuid:id>", views.SampleDetail.as_view(), name="sample-detail"),
                path("<uuid:id>/edit", views.SampleEdit.as_view(), name="sample-edit"),
            ]
        ),
    ),
]
