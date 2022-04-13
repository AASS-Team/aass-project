from django.shortcuts import redirect
from django.contrib import messages
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

from . import serializers
from .models import Grant


class GrantList(APIView):

    """
    List all grants, or create a new grant.
    """

    serializer_class = serializers.GrantSerializer
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, format=None):
        grants = Grant.objects.all()
        serializer = self.serializer_class(grants, many=True)

        options = {
            "data": {
                "items": grants,
                "onclick": "grant-detail",
                "empty": "Ľutujeme, nenašli sa žiadne granty",
            },
            "header": {
                "items": [
                    {"name": "názov grantu", "key": "name"},
                ]
            },
            "layout": [
                {"left": True},
            ],
        }

        return Response(
            data={"grants": serializer.data, "options": options},
            template_name="grants/index.html",
        )

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            messages.add_message(
                request, messages.ERROR, "Nepodarilo sa uložiť analýzu"
            )
            return Response(
                data={
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
                template_name="grants/create.html",
            )

        messages.add_message(request, messages.SUCCESS, "Grant uložený")
        serializer.save()
        return redirect("grant-list")


class GrantCreate(APIView):
    """
    Create new grant
    """

    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, format=None):

        return Response(
            template_name="grants/create.html",
        )


class GrantDetail(APIView):
    """
    Grant detail
    """

    renderer_classes = [TemplateHTMLRenderer]

    def get_object(self, id):
        try:
            return Grant.objects.get(pk=id)
        except Grant.DoesNotExist:
            return redirect("404")

    def get(self, request, id, format=None):
        grant = self.get_object(id)
        serializer = serializers.GrantSerializer(grant)
        return Response(
            data={"grant": serializer.data}, template_name="grants/detail.html"
        )

    def put(self, request, id, format=None):
        grant = self.get_object(id)
        serializer = serializers.GrantSerializer(grant, data=request.data)

        if not serializer.is_valid():
            messages.add_message(request, messages.ERROR, "Nepodarilo sa uložiť grant")
            return Response(
                data={
                    "grant": serializer.data,
                },
                template_name="grants/edit.html",
            )

        serializer.save()
        messages.add_message(request, messages.SUCCESS, "Grant uložený")
        return Response(
            data={"grant": serializer.data}, template_name="grants/detail.html"
        )

    def delete(self, request, id, format=None):
        grant = self.get_object(id)
        deleted_rows = grant.delete()

        if len(deleted_rows) <= 0:
            messages.add_message(request, messages.ERROR, "Chyba!")
            return redirect("grant-detail", id)

        messages.add_message(request, messages.SUCCESS, "Grant vymazaný")
        return redirect("grant-list")


class GrantEdit(APIView):
    """
    Grant edit
    """

    renderer_classes = [TemplateHTMLRenderer]

    def get_object(self, id):
        try:
            return Grant.objects.get(pk=id)
        except Grant.DoesNotExist:
            return redirect("404")

    def get(self, request, id, format=None):
        grant = self.get_object(id)
        serializer = serializers.GrantSerializer(grant)

        return Response(
            data={
                "grant": serializer.data,
            },
            template_name="grants/edit.html",
        )
