from django.urls import include, path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    path(
        "labs/",
        include([]),
    ),
]
