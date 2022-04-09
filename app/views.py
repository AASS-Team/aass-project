from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

from . import serializers
from .models import Sample


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
            {"samples": serializer.data, "options": options},
            template_name="samples/index.html",
        )
