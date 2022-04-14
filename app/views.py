from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.shortcuts import redirect
from rest_framework.views import APIView


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
