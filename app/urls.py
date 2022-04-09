from django.urls import include, path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path("", RedirectView.as_view(url="samples", permanent=False)),
    path(
        "samples/",
        include(
            [
                path("", views.SampleList.as_view()),
            ]
        ),
    ),
]
