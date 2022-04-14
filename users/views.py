from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.contrib import messages
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

from .models import User
from . import serializers


class UserList(LoginRequiredMixin, APIView):
    """
    List all users, or create a new user.
    """

    serializer_class = serializers.UserSerializer
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, format=None):
        users = User.objects.all()
        serializer = self.serializer_class(users, many=True)
        options = {
            "data": {
                "items": users,
                "onclick": "user-detail",
                "empty": "Ľutujeme, nenašli sa žiadni používatelia",
            },
            "header": {
                "items": [
                    {"name": "meno", "key": "name"},
                    {"name": "e-mail", "key": "email"},
                ]
            },
            "layout": [
                {"width": 96, "width-sm": 64, "left": True},
            ],
        }

        return Response(
            data={"users": serializer.data, "options": options},
            template_name="users/index.html",
        )

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            messages.add_message(
                request, messages.ERROR, "Nepodarilo sa uložiť používateľa"
            )
            return Response(
                data={
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
                template_name="users/create.html",
            )

        messages.add_message(request, messages.SUCCESS, "Používteľ uložený")
        serializer.save()
        return redirect("user-list")


class UserCreate(LoginRequiredMixin, APIView):
    """
    Create new user
    """

    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, format=None):
        groups = serializers.GroupSerializer(Group.objects.all(), many=True)

        return Response(
            data={"groups": groups.data},
            template_name="users/create.html",
        )


class UserDetail(LoginRequiredMixin, APIView):
    """
    User detail
    """

    renderer_classes = [TemplateHTMLRenderer]

    def get_object(self, id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            return redirect("404")

    def get(self, request, id, format=None):
        user = self.get_object(id)
        serializer = serializers.UserSerializer(user)
        return Response(
            data={"user": serializer.data}, template_name="users/detail.html"
        )

    def put(self, request, id, format=None):
        user = self.get_object(id)
        serializer = serializers.UserSerializer(user, data=request.data)

        if not serializer.is_valid():
            messages.add_message(
                request, messages.ERROR, "Nepodarilo sa uložiť používateľa"
            )
            return Response(
                data={
                    "user": serializer.data,
                },
                template_name="users/edit.html",
            )

        serializer.save()
        messages.add_message(request, messages.SUCCESS, "Používateľ uložený")
        return Response(
            data={"user": serializer.data}, template_name="users/detail.html"
        )

    def delete(self, request, id, format=None):
        user = self.get_object(id)
        deleted_rows = user.delete()

        if len(deleted_rows) <= 0:
            messages.add_message(request, messages.ERROR, "Chyba!")
            return redirect("user-detail", id)

        messages.add_message(request, messages.SUCCESS, "Používateľ vymazaný")
        return redirect("user-list")


class UserEdit(LoginRequiredMixin, APIView):
    """
    user edit
    """

    renderer_classes = [TemplateHTMLRenderer]

    def get_object(self, id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            return redirect("404")

    def get(self, request, id, format=None):
        user = self.get_object(id)
        serializer = serializers.UserSerializer(user)
        groups = serializers.GroupSerializer(Group.objects.all(), many=True)

        return Response(
            data={
                "user": serializer.data,
                "groups": groups.data,
            },
            template_name="users/edit.html",
        )
