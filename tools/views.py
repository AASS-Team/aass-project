from django.contrib.auth.decorators import permission_required
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

from . import serializers
from tools.models import Tool


class ToolList(APIView):
    """
    List all tools, or create a new tool.
    """

    serializer_class = serializers.ToolSerializer
    renderer_classes = [TemplateHTMLRenderer]

    @method_decorator(permission_required("tools.view_tool", raise_exception=True))
    def get(self, request, format=None):
        tools = Tool.objects.all()
        serializer = self.serializer_class(tools, many=True)
        options = {
            "data": {
                "items": tools,
                "onclick": "tool-detail",
                "empty": "Ľutujeme, nenašli sa žiadne nástroje",
            },
            "header": {
                "items": [
                    {
                        "name": "",
                        "key": "status",
                    },
                    {"name": "názov", "key": "name"},
                    {"name": "typ", "key": "type"},
                    {"name": "stav", "key": "available"},
                ]
            },
            "layout": [
                {"width": 8},
                {"width": 96, "width-sm": 64, "left": True},
            ],
        }

        return Response(
            data={"tools": serializer.data, "options": options},
            template_name="tools/index.html",
        )

    @method_decorator(permission_required("tools.add_tool", raise_exception=True))
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            tools = serializers.ToolSerializer(Tool.objects.all(), many=True)

            messages.add_message(
                request, messages.ERROR, "Nepodarilo sa uložiť nástroj"
            )
            tools
            return Response(
                data={
                    "tools": tools.data,
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
                template_name="tools/create.html",
            )

        messages.add_message(request, messages.SUCCESS, "Nástroj uložený")
        serializer.save(available=True)
        return redirect("tool-list")


class ToolCreate(APIView):
    """
    Create new tool
    """

    renderer_classes = [TemplateHTMLRenderer]

    @method_decorator(permission_required("tools.add_tool", raise_exception=True))
    def get(self, request, format=None):

        return Response(
            template_name="tools/create.html",
        )


class ToolDetail(APIView):
    """
    Tool detail
    """

    renderer_classes = [TemplateHTMLRenderer]

    def get_object(self, id):
        try:
            return Tool.objects.get(pk=id)
        except Tool.DoesNotExist:
            return redirect("404")

    @method_decorator(permission_required("tools.view_tool", raise_exception=True))
    def get(self, request, id, format=None):
        tool = self.get_object(id)
        serializer = serializers.ToolSerializer(tool)
        return Response(
            data={"tool": serializer.data}, template_name="tools/detail.html"
        )

    @method_decorator(permission_required("tools.change_tool", raise_exception=True))
    def put(self, request, id, format=None):
        tool = self.get_object(id)
        serializer = serializers.ToolSerializer(tool, data=request.data)

        if not serializer.is_valid():
            messages.add_message(
                request, messages.ERROR, "Nepodarilo sa uložiť nástroj"
            )
            return Response(
                data={
                    "tool": serializer.data,
                },
                template_name="tools/edit.html",
            )

        serializer.save()
        messages.add_message(request, messages.SUCCESS, "Nástroj uložený")
        return Response(
            data={"tool": serializer.data}, template_name="tools/detail.html"
        )

    @method_decorator(permission_required("tools.delete_tool", raise_exception=True))
    def delete(self, request, id, format=None):
        tool = self.get_object(id)
        deleted_rows = tool.delete()

        if len(deleted_rows) <= 0:
            messages.add_message(request, messages.ERROR, "Chyba!")
            return redirect("tool-detail", id)

        messages.add_message(request, messages.SUCCESS, "Nástroj vymazaný")
        return redirect("tool-list")


class ToolEdit(APIView):
    """
    Tool edit
    """

    renderer_classes = [TemplateHTMLRenderer]

    def get_object(self, id):
        try:
            return Tool.objects.get(pk=id)
        except Tool.DoesNotExist:
            return redirect("404")

    @method_decorator(permission_required("tools.change_tool", raise_exception=True))
    def get(self, request, id, format=None):
        tool = self.get_object(id)
        serializer = serializers.ToolSerializer(tool)

        return Response(
            data={
                "tool": serializer.data,
            },
            template_name="tools/edit.html",
        )
