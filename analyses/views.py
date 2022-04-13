from django.shortcuts import redirect
from django.contrib import messages
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

from . import serializers
from app.serializers import ToolSerializer
from app.models import Sample, User, Lab, Tool
from .models import Analysis


class AnalysisList(APIView):

    """
    List all analyses, or create a new analysis.
    """

    serializer_class = serializers.AnalysisSerializer
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, format=None):
        analyses = Analysis.objects.all()
        serializer = self.serializer_class(analyses, many=True)

        options = {
            "data": {
                "items": analyses,
                "onclick": "analysis-detail",
                "empty": "Ľutujeme, nenašli sa žiadne analýzy",
            },
            "header": {
                "items": [
                    # TODO status icon
                    {
                        "name": "stav",
                        "key": "status",
                    },
                    {"name": "vzorka", "key": "sample"},
                ]
            },
            "layout": [
                {"width": 8},
                {"width": 96, "width-sm": 64, "left": True},
            ],
        }

        return Response(
            data={"analyses": serializer.data, "options": options},
            template_name="analyses/index.html",
        )

    def post(self, request, format=None):

        serializer = self.serializer_class(
            data=request.data,
        )

        if not serializer.is_valid():
            samples = serializers.SampleSerializer(Sample.objects.all(), many=True)
            lab = serializers.LabSerializer(Lab.objects.all(), many=True)
            users = serializers.UserSerializer(User.objects.all(), many=True)
            tools = ToolSerializer(Tool.objects.all(), many=True)

            messages.add_message(
                request, messages.ERROR, "Nepodarilo sa uložiť analýzu"
            )
            return Response(
                data={
                    "samples": samples.data,
                    "labs": lab.data,
                    "laborants": users.data,
                    "tools": tools.data,
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
                template_name="analyses/create.html",
            )

        messages.add_message(request, messages.SUCCESS, "Analýza uložená")
        serializer.save(status=Analysis.Status.PENDING)
        return redirect("analysis-list")


# loads data to select boxes
class AnalysisCreate(APIView):
    """
    Create new analysis
    """

    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, format=None):
        labs = serializers.LabSerializer(Lab.objects.all(), many=True)
        samples = serializers.SampleSerializer(Sample.objects.all(), many=True)
        users = serializers.UserSerializer(User.objects.all(), many=True)
        tools = ToolSerializer(Tool.objects.all(), many=True)

        return Response(
            data={
                "samples": samples.data,
                "labs": labs.data,
                "laborants": users.data,
                "tools": tools.data,
            },
            template_name="analyses/create.html",
        )


class AnalysisDetail(APIView):
    """
    Analysis detail
    """

    renderer_classes = [TemplateHTMLRenderer]

    def get_object(self, id):
        try:
            return Analysis.objects.get(pk=id)
        except Analysis.DoesNotExist:
            return redirect("404")

    def get(self, request, id, format=None):
        analysis = self.get_object(id)
        serializer = serializers.AnalysisSerializer(analysis)
        return Response(
            data={"analysis": serializer.data}, template_name="analyses/detail.html"
        )

    def put(self, request, id, format=None):
        analysis = self.get_object(id)
        serializer = serializers.AnalysisSerializer(analysis, data=request.data)

        if not serializer.is_valid():

            messages.add_message(request, messages.ERROR, "Nepodarilo sa uložiť vzorku")
            return Response(
                data={
                    "sample": serializer.data,
                    # "users": users.data,
                    # "grants": grants.data,
                },
                template_name="analyses/edit.html",
            )

        serializer.save()
        messages.add_message(request, messages.SUCCESS, "Analýza uložená")
        return Response(
            data={"analysis": serializer.data}, template_name="analyses/detail.html"
        )

    def delete(self, request, id, format=None):
        analysis = self.get_object(id)
        deleted_rows = analysis.delete()

        if len(deleted_rows) <= 0:
            messages.add_message(request, messages.ERROR, "Chyba!")
            return redirect("analysis-detail", id)

        messages.add_message(request, messages.SUCCESS, "Analýza vymazaná")
        return redirect("analysis-list")


class AnalysisEdit(APIView):
    """
    Analysis edit
    """

    renderer_classes = [TemplateHTMLRenderer]

    def get_object(self, id):
        try:
            return Analysis.objects.get(pk=id)
        except Analysis.DoesNotExist:
            return redirect("404")

    def get(self, request, id, format=None):
        analysis = self.get_object(id)
        serializer = serializers.AnalysisSerializer(analysis)
        labs = serializers.LabSerializer(Lab.objects.all(), many=True)
        samples = serializers.SampleSerializer(Sample.objects.all(), many=True)
        users = serializers.UserSerializer(User.objects.all(), many=True)
        tools = ToolSerializer(Tool.objects.all(), many=True)

        return Response(
            data={
                "analysis": serializer.data,
                "samples": samples.data,
                "labs": labs.data,
                "laborants": users.data,
                "tools": tools.data,
            },
            template_name="analyses/edit.html",
        )
