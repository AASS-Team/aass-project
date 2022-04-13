from django.shortcuts import redirect
from django.contrib import messages
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

from .models import User, Role
from . import serializers


class UserList(APIView):
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
                    {"name": "názov", "key": "name"},
                    {"name": "používateľ", "key": "login"},
                    {
                        "name": "dátum",
                        "key": "created_at",
                    },
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
            roles = serializers.RoleSerializer(Role.objects.all(), many=True)
            messages.add_message(
                request, messages.ERROR, "Nepodarilo sa uložiť používateľa"
            )
            return Response(
                data={
                    "roles": roles.data,
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
                template_name="users/create.html",
            )

        messages.add_message(request, messages.SUCCESS, "Používteľ uložený")
        serializer.save()
        return redirect("user-list")


class UserCreate(APIView):
    """
    Create new user
    """

    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, format=None):
        roles = serializers.RoleSerializer(Role.objects.all(), many=True)

        return Response(
            data={"roles": roles.data},
            template_name="users/create.html",
        )


class UserDetail(APIView):
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


class UserEdit(APIView):
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
        roles = serializers.RoleSerializer(Role.objects.all(), many=True)

        return Response(
            data={
                "roles": roles.data,
                "user": serializer.data,
            },
            template_name="users/edit.html",
        )
