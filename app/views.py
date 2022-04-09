from django.shortcuts import redirect
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

from . import serializers
from .models import Sample, User, Grant


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
                "onclick": "/samples/",
                "empty": "Ľutujeme, nenašli sa žiadne vzorky",
            },
            "header": {
                "items": [
                    {"name": "id"},
                    {"name": "názov", "key": "name"},
                    {"name": "používateľ", "key": "login"},
                    {
                        "name": "dátum",
                        "key": "created_at",
                    },
                ]
            },
            "layout": [
                {
                    "width": 16,
                },
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
            return Response(
                data={
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
                template_name="samples/create.html",
            )
        else:
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
            data={"users": users.data, "grants": grants.data}, template_name="samples/create.html"
        )
