from django.urls import include, path

from . import views

urlpatterns = [
    path(
        "users/",
        include(
            [
                path("", views.UserList.as_view(), name="user-list"),
                path("new", views.UserCreate.as_view(), name="user-new"),
                path("<uuid:id>", views.UserDetail.as_view(), name="user-detail"),
                path("<uuid:id>/edit", views.UserEdit.as_view(), name="user-edit"),
            ]
        ),
    ),
]
