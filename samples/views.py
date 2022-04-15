from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

from . import serializers
from .models import Sample
from grants.models import Grant
from users.models import User


class SampleList(LoginRequiredMixin, APIView):
    """
    List all samples, or create a new sample.
    """

    serializer_class = serializers.SampleSerializer
    renderer_classes = [TemplateHTMLRenderer]

    @method_decorator(permission_required("samples.view_sample", raise_exception=True))
    def get(self, request, format=None):
        if request.user.groups.filter(name__in=["admin", "laborant"]).exists():
            samples = Sample.objects.all()
        else:
            samples = Sample.objects.filter(user=request.user.id)

        serializer = self.serializer_class(samples, many=True)
        options = {
            "data": {
                "items": samples,
                "onclick": "sample-detail",
                "empty": "Ľutujeme, nenašli sa žiadne vzorky",
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
            data={"samples": serializer.data, "options": options},
            template_name="samples/index.html",
        )

    @method_decorator(permission_required("samples.add_sample", raise_exception=True))
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            users = serializers.UserSerializer(User.objects.all(), many=True)
            grants = serializers.GrantSerializer(Grant.objects.all(), many=True)

            messages.add_message(request, messages.ERROR, "Nepodarilo sa uložiť vzorku")
            return Response(
                data={
                    "users": users.data,
                    "grants": grants.data,
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
                template_name="samples/create.html",
            )

        messages.add_message(request, messages.SUCCESS, "Vzorka uložená")
        serializer.save()
        return redirect("sample-list")


class SampleCreate(LoginRequiredMixin, APIView):
    """
    Create new sample
    """

    renderer_classes = [TemplateHTMLRenderer]

    @method_decorator(permission_required("samples.add_sample", raise_exception=True))
    def get(self, request, format=None):
        users = serializers.UserSerializer(User.objects.all(), many=True)
        grants = serializers.GrantSerializer(Grant.objects.all(), many=True)

        return Response(
            data={"users": users.data, "grants": grants.data},
            template_name="samples/create.html",
        )


class SampleDetail(LoginRequiredMixin, APIView):
    """
    Sample detail
    """

    renderer_classes = [TemplateHTMLRenderer]

    def get_object(self, id):
        try:
            return Sample.objects.get(pk=id)
        except Sample.DoesNotExist:
            return redirect("404")

    @method_decorator(permission_required("samples.view_sample", raise_exception=True))
    def get(self, request, id, format=None):
        sample = self.get_object(id)

        if (
            not request.user.groups.filter(name__in=["admin", "laborant"]).exists()
            and request.user.id != sample.user.id
        ):
            raise PermissionDenied()

        serializer = serializers.SampleSerializer(sample)
        return Response(
            data={"sample": serializer.data}, template_name="samples/detail.html"
        )

    @method_decorator(
        permission_required("samples.change_sample", raise_exception=True)
    )
    def put(self, request, id, format=None):
        sample = self.get_object(id)
        serializer = serializers.SampleSerializer(sample, data=request.data)

        if not serializer.is_valid():
            users = serializers.UserSerializer(User.objects.all(), many=True)
            grants = serializers.GrantSerializer(Grant.objects.all(), many=True)

            messages.add_message(request, messages.ERROR, "Nepodarilo sa uložiť vzorku")
            return Response(
                data={
                    "sample": serializer.data,
                    "users": users.data,
                    "grants": grants.data,
                },
                template_name="samples/edit.html",
            )

        serializer.save()
        messages.add_message(request, messages.SUCCESS, "Vzorka uložená")
        return Response(
            data={"sample": serializer.data}, template_name="samples/detail.html"
        )

    @method_decorator(
        permission_required("samples.delete_sample", raise_exception=True)
    )
    def delete(self, request, id, format=None):
        sample = self.get_object(id)
        deleted_rows = sample.delete()

        if len(deleted_rows) <= 0:
            messages.add_message(request, messages.ERROR, "Chyba!")
            return redirect("sample-detail", id)

        messages.add_message(request, messages.SUCCESS, "Vzorka vymazaná")
        return redirect("sample-list")


class SampleEdit(LoginRequiredMixin, APIView):
    """
    Sample edit
    """

    renderer_classes = [TemplateHTMLRenderer]

    def get_object(self, id):
        try:
            return Sample.objects.get(pk=id)
        except Sample.DoesNotExist:
            return redirect("404")

    @method_decorator(
        permission_required("samples.change_sample", raise_exception=True)
    )
    def get(self, request, id, format=None):
        sample = self.get_object(id)
        serializer = serializers.SampleSerializer(sample)
        users = serializers.UserSerializer(User.objects.all(), many=True)
        grants = serializers.GrantSerializer(Grant.objects.all(), many=True)

        return Response(
            data={
                "sample": serializer.data,
                "users": users.data,
                "grants": grants.data,
            },
            template_name="samples/edit.html",
        )
