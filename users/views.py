from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.exceptions import NotFound
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

    @method_decorator(permission_required("users.view_user", raise_exception=True))
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
                    {"name": "rola", "key": "groups"},
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

    @method_decorator(permission_required("users.add_user", raise_exception=True))
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            groups = serializers.GroupSerializer(Group.objects.all(), many=True)
            messages.add_message(
                request, messages.ERROR, "Nepodarilo sa uložiť používateľa"
            )
            return Response(
                data={
                    "groups": groups.data,
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

    @method_decorator(permission_required("users.add_user", raise_exception=True))
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
            raise NotFound()

    @method_decorator(permission_required("users.view_user", raise_exception=True))
    def get(self, request, id, format=None):
        user = self.get_object(id)
        serializer = serializers.UserSerializer(user)
        return Response(
            data={"user": serializer.data}, template_name="users/detail.html"
        )

    @method_decorator(permission_required("users.change_user", raise_exception=True))
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

    @method_decorator(permission_required("users.delete_user", raise_exception=True))
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
            raise NotFound()

    @method_decorator(permission_required("users.change_user", raise_exception=True))
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
