from django.urls import include, path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    # path("", RedirectView.as_view(url="samples", permanent=False)),
    path(
        "grants/",
        include(
            [
                path("", views.GrantList.as_view(), name="grant-list"),
                path("new", views.GrantCreate.as_view(), name="grant-new"),
                path("<uuid:id>", views.GrantDetail.as_view(), name="grant-detail"),
                path("<uuid:id>/edit", views.GrantEdit.as_view(), name="grant-edit"),
            ]
        ),
    ),
]
