from django.shortcuts import redirect
from django.contrib import messages
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

from . import serializers
from .models import Sample
from grants.models import Grant
from users.models import User


class SampleList(APIView):
    """
    List all samples, or create a new sample.
    """

    serializer_class = serializers.SampleSerializer
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, format=None):
        samples = Sample.objects.all()
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


class SampleCreate(APIView):
    """
    Create new sample
    """

    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, format=None):
        users = serializers.UserSerializer(User.objects.all(), many=True)
        grants = serializers.GrantSerializer(Grant.objects.all(), many=True)

        return Response(
            data={"users": users.data, "grants": grants.data},
            template_name="samples/create.html",
        )


class SampleDetail(APIView):
    """
    Sample detail
    """

    renderer_classes = [TemplateHTMLRenderer]

    def get_object(self, id):
        try:
            return Sample.objects.get(pk=id)
        except Sample.DoesNotExist:
            return redirect("404")

    def get(self, request, id, format=None):
        sample = self.get_object(id)
        serializer = serializers.SampleSerializer(sample)
        return Response(
            data={"sample": serializer.data}, template_name="samples/detail.html"
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

    def delete(self, request, id, format=None):
        sample = self.get_object(id)
        deleted_rows = sample.delete()

        if len(deleted_rows) <= 0:
            messages.add_message(request, messages.ERROR, "Chyba!")
            return redirect("sample-detail", id)

        messages.add_message(request, messages.SUCCESS, "Vzorka vymazaná")
        return redirect("sample-list")


class SampleEdit(APIView):
    """
    Sample edit
    """

    renderer_classes = [TemplateHTMLRenderer]

    def get_object(self, id):
        try:
            return Sample.objects.get(pk=id)
        except Sample.DoesNotExist:
            return redirect("404")

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