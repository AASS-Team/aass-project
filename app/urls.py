from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path(
        "login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"
    ),
    path(
        "change-password/",
        auth_views.PasswordChangeView.as_view(template_name="change-password.html"),
        name="change-password",
    ),
    path(
        "change-password/done",
        views.PasswordChangeDone.as_view(),
        name="password_change_done",
    ),
    path("logout/", views.Logout.as_view(), name="logout"),
    path("administration/", views.Administration.as_view(), name="administration")
]
