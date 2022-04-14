from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer


class Logout(LoginRequiredMixin, APIView):
    """
    Logout
    """

    def get(self, request, format=None):
        logout(request)
        return redirect("login")


class PasswordChangeDone(LoginRequiredMixin, APIView):
    """
    Password change done redirect
    """

    def get(self, request, format=None):
        messages.add_message(request, messages.SUCCESS, "Heslo úspešne zmenené.")
        return redirect("change-password")


class Administration(LoginRequiredMixin, APIView):
    """
    Administration router
    """
    renderer_classes = [TemplateHTMLRenderer]

    # @method_decorator(permission_required("app.view_administration", raise_exception=True))
    def get(self, request, format=None):
        return Response(
            template_name="administration/index.html",
        )
