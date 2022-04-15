from django.contrib.auth.decorators import permission_required
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

from . import serializers
from labs.models import Lab

class LabsList(APIView):
    """
    List all labs, or create a new lab.
    """

    serializer_class = serializers.LabSerializer
    renderer_classes = [TemplateHTMLRenderer]

    @method_decorator(permission_required("labs.view_lab", raise_exception=True))
    def get(self, request, format=None):
        labs = Lab.objects.all()
        serializer = self.serializer_class(labs, many=True)
        options = {
            "data": {
                "items": labs,
                "onclick": "lab-detail",
                "empty": "Ľutujeme, nenašli sa žiadne laboratória",
            },
            "header": {
                "items": [
                    {
                        "name": "",
                        "key": "status",
                    },
                    {"name": "názov", "key": "name"},
                    {"name": "adresa", "key": "address"},
                    {"name": "stav", "key": "available"},
                ]
            },
            "layout": [
                {"width": 8},
                {"width": 96, "width-sm": 64, "left": True},
            ],
        }

        return Response(
            data={"labs": serializer.data, "options": options},
            template_name="labs/index.html",
        )

    @method_decorator(permission_required("labs.add_lab", raise_exception=True))
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            labs = serializers.LabSerializer(Lab.objects.all(), many=True)

            messages.add_message(
                request, messages.ERROR, "Nepodarilo sa uložiť laboratórium"
            )
            return Response(
                data={
                    "labs": labs.data,
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
                template_name="labs/create.html",
            )

        messages.add_message(request, messages.SUCCESS, "Laboratórium uložené")
        serializer.save(available=True)
        return redirect("lab-list")


class LabCreate(APIView):
    """
    Create new lab
    """

    renderer_classes = [TemplateHTMLRenderer]

    @method_decorator(permission_required("labs.add_lab", raise_exception=True))
    def get(self, request, format=None):

        return Response(
            template_name="labs/create.html",
        )


class LabDetail(APIView):
    """
    Lab detail
    """

    renderer_classes = [TemplateHTMLRenderer]

    def get_object(self, id):
        try:
            return Lab.objects.get(pk=id)
        except Lab.DoesNotExist:
            return redirect("404")

    @method_decorator(permission_required("labs.view_lab", raise_exception=True))
    def get(self, request, id, format=None):
        lab = self.get_object(id)
        serializer = serializers.LabSerializer(lab)
        return Response(data={"lab": serializer.data}, template_name="labs/detail.html")

    @method_decorator(permission_required("labs.change_lab", raise_exception=True))
    def put(self, request, id, format=None):
        lab = self.get_object(id)
        serializer = serializers.LabSerializer(lab, data=request.data)

        if not serializer.is_valid():
            messages.add_message(
                request, messages.ERROR, "Nepodarilo sa uložiť laboratórium"
            )
            return Response(
                data={
                    "lab": serializer.data,
                },
                template_name="labs/edit.html",
            )

        serializer.save()
        messages.add_message(request, messages.SUCCESS, "Laboratórium uložené")
        return Response(data={"lab": serializer.data}, template_name="labs/detail.html")

    @method_decorator(permission_required("labs.delete_lab", raise_exception=True))
    def delete(self, request, id, format=None):
        lab = self.get_object(id)
        deleted_rows = lab.delete()

        if len(deleted_rows) <= 0:
            messages.add_message(request, messages.ERROR, "Chyba!")
            return redirect("lab-detail", id)

        messages.add_message(request, messages.SUCCESS, "Laboratórium vymazané")
        return redirect("lab-list")


class LabEdit(APIView):
    """
    Lab edit
    """

    renderer_classes = [TemplateHTMLRenderer]

    def get_object(self, id):
        try:
            return Lab.objects.get(pk=id)
        except Lab.DoesNotExist:
            return redirect("404")

    @method_decorator(permission_required("labs.change_lab", raise_exception=True))
    def get(self, request, id, format=None):
        lab = self.get_object(id)
        serializer = serializers.LabSerializer(lab)

        return Response(
            data={
                "lab": serializer.data,
            },
            template_name="labs/edit.html",
        )
