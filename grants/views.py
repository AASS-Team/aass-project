from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

from . import serializers
from .models import Grant


class GrantList(LoginRequiredMixin, APIView):

    """
    List all grants, or create a new grant.
    """

    serializer_class = serializers.GrantSerializer
    renderer_classes = [TemplateHTMLRenderer]

    @method_decorator(permission_required("grants.view_grant", raise_exception=True))
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

    @method_decorator(permission_required("grants.add_grant", raise_exception=True))
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            messages.add_message(request, messages.ERROR, "Nepodarilo sa uložiť grant")
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


class GrantCreate(LoginRequiredMixin, APIView):
    """
    Create new grant
    """

    renderer_classes = [TemplateHTMLRenderer]

    @method_decorator(permission_required("grants.add_grant", raise_exception=True))
    def get(self, request, format=None):

        return Response(
            template_name="grants/create.html",
        )


class GrantDetail(LoginRequiredMixin, APIView):
    """
    Grant detail
    """

    renderer_classes = [TemplateHTMLRenderer]

    def get_object(self, id):
        try:
            return Grant.objects.get(pk=id)
        except Grant.DoesNotExist:
            return redirect("404")

    @method_decorator(permission_required("grants.view_grant", raise_exception=True))
    def get(self, request, id, format=None):
        grant = self.get_object(id)
        serializer = serializers.GrantSerializer(grant)
        return Response(
            data={"grant": serializer.data}, template_name="grants/detail.html"
        )

    @method_decorator(permission_required("grants.change_grant", raise_exception=True))
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

    @method_decorator(permission_required("grants.delete_grant", raise_exception=True))
    def delete(self, request, id, format=None):
        grant = self.get_object(id)
        deleted_rows = grant.delete()

        if len(deleted_rows) <= 0:
            messages.add_message(request, messages.ERROR, "Chyba!")
            return redirect("grant-detail", id)

        messages.add_message(request, messages.SUCCESS, "Grant vymazaný")
        return redirect("grant-list")


class GrantEdit(LoginRequiredMixin, APIView):
    """
    Grant edit
    """

    renderer_classes = [TemplateHTMLRenderer]

    def get_object(self, id):
        try:
            return Grant.objects.get(pk=id)
        except Grant.DoesNotExist:
            return redirect("404")

    @method_decorator(permission_required("grants.change_grant", raise_exception=True))
    def get(self, request, id, format=None):
        grant = self.get_object(id)
        serializer = serializers.GrantSerializer(grant)

        return Response(
            data={
                "grant": serializer.data,
            },
            template_name="grants/edit.html",
        )
