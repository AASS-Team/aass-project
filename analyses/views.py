from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.contrib import messages
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

from .models import Analysis
from .serializers import AnalysisSerializer
from samples.models import Sample
from samples.serializers import SampleSerializer
from users.models import User
from users.serializers import UserSerializer
from tools.models import Tool
from tools.serializers import ToolSerializer
from labs.models import Lab
from labs.serializers import LabSerializer


class AnalysisList(LoginRequiredMixin, APIView):
    """
    List all analyses, or create a new analysis.
    """

    serializer_class = AnalysisSerializer
    renderer_classes = [TemplateHTMLRenderer]

    @method_decorator(
        permission_required("analyses.view_analysis", raise_exception=True)
    )
    def get(self, request, format=None):
        if request.user.groups.filter(name__in=["administrátor", "laborant"]).exists():
            analyses = Analysis.objects.all()
        else:
            analyses = Analysis.objects.filter(sample__user__id=request.user.id)

        serializer = self.serializer_class(analyses, many=True)

        options = {
            "data": {
                "items": analyses,
                "onclick": "analysis-detail",
                "empty": "Ľutujeme, nenašli sa žiadne analýzy",
            },
            "header": {
                "items": [
                    {
                        "name": "",
                        "key": "status",
                    },
                    {"name": "vzorka", "key": "sample"},
                    {"name": "stav", "key": "status"},
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

    @method_decorator(
        permission_required("analyses.add_analysis", raise_exception=True)
    )
    def post(self, request, format=None):
        serializer = self.serializer_class(
            data=request.data,
        )

        if not serializer.is_valid():
            samples = SampleSerializer(
                Sample.objects.filter(Q(analysis__isnull=True)), many=True
            )
            lab = LabSerializer(Lab.objects.all(), many=True)
            users = UserSerializer(
                User.objects.filter(~Q(groups__name="používateľ")), many=True
            )
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

        # set tools unavailable
        tools = serializer.validated_data.get("tools")
        for tool in tools:
            tool.available = False
        Tool.objects.bulk_update(tools, ["available"])

        # set lab as unavailable
        lab = serializer.validated_data.get("lab")
        lab.available = False
        lab.save()

        messages.add_message(request, messages.SUCCESS, "Analýza uložená")
        serializer.save(status=Analysis.Status.PENDING)
        return redirect("analysis-list")


# loads data to select boxes
class AnalysisCreate(LoginRequiredMixin, APIView):
    """
    Create new analysis
    """

    renderer_classes = [TemplateHTMLRenderer]

    @method_decorator(
        permission_required("analyses.add_analysis", raise_exception=True)
    )
    def get(self, request, format=None):
        labs = LabSerializer(Lab.objects.all(), many=True)
        samples = SampleSerializer(
            Sample.objects.filter(analysis__isnull=True), many=True
        )
        users = UserSerializer(
            User.objects.filter(~Q(groups__name="používateľ")), many=True
        )
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


class AnalysisDetail(LoginRequiredMixin, APIView):
    """
    Analysis detail
    """

    renderer_classes = [TemplateHTMLRenderer]

    def get_object(self, id):
        try:
            return Analysis.objects.get(pk=id)
        except Analysis.DoesNotExist:
            raise NotFound()

    @method_decorator(
        permission_required("analyses.view_analysis", raise_exception=True)
    )
    def get(self, request, id, format=None):
        analysis = self.get_object(id)

        if (
            not request.user.groups.filter(
                name__in=["administrátor", "laborant"]
            ).exists()
            and request.user.id != analysis.sample.user.id
        ):
            raise PermissionDenied()

        serializer = AnalysisSerializer(analysis)
        return Response(
            data={"analysis": serializer.data}, template_name="analyses/detail.html"
        )

    @method_decorator(
        permission_required("analyses.change_analysis", raise_exception=True)
    )
    def put(self, request, id, format=None):
        analysis = self.get_object(id)
        serializer = AnalysisSerializer(analysis, data=request.data)

        if not serializer.is_valid():
            labs = LabSerializer(Lab.objects.all(), many=True)
            samples = SampleSerializer(
                Sample.objects.filter(
                    Q(analysis__isnull=True) | Q(id=analysis.sample.id)
                ),
                many=True,
            )
            users = UserSerializer(
                User.objects.filter(~Q(groups__name="používateľ")), many=True
            )
            tools = ToolSerializer(Tool.objects.all(), many=True)

            messages.add_message(request, messages.ERROR, "Nepodarilo sa uložiť vzorku")
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

        # update tool availability
        old_tools = list(analysis.tools.all())
        new_tools = serializer.validated_data.get("tools")

        removed_tools = frozenset(old_tools).difference(new_tools)
        for tool in removed_tools:  # Removed tools
            tool.available = True

        added_tools = frozenset(new_tools).difference(old_tools)
        for tool in added_tools:
            tool.available = False

        changed_tools = [*removed_tools, *added_tools]
        if len(changed_tools) > 0:
            Tool.objects.bulk_update(changed_tools, ["available"])

        # update lab availability
        old_lab = analysis.lab
        new_lab = serializer.validated_data.get("lab")

        if old_lab is not new_lab:
            old_lab.available, new_lab.available = (
                new_lab.available,
                old_lab.available,
            )  # swap availability
            Lab.objects.bulk_update([old_lab, new_lab], ["available"])

        serializer.save()
        messages.add_message(request, messages.SUCCESS, "Analýza uložená")
        return Response(
            data={"analysis": serializer.data}, template_name="analyses/detail.html"
        )

    @method_decorator(
        permission_required("analyses.delete_analysis", raise_exception=True)
    )
    def delete(self, request, id, format=None):
        analysis = self.get_object(id)
        tools = list(analysis.tools.all())
        lab = analysis.lab
        deleted_rows = analysis.delete()

        if len(deleted_rows) <= 0:
            messages.add_message(request, messages.ERROR, "Chyba!")
            return redirect("analysis-detail", id)

        # set tools as available
        for tool in tools:
            tool.available = True
        Tool.objects.bulk_update(tools, ["available"])

        # set lab as available
        lab.available = True
        lab.save()

        messages.add_message(request, messages.SUCCESS, "Analýza vymazaná")
        return redirect("analysis-list")


class AnalysisEdit(LoginRequiredMixin, APIView):
    """
    Analysis edit
    """

    renderer_classes = [TemplateHTMLRenderer]

    def get_object(self, id):
        try:
            return Analysis.objects.get(pk=id)
        except Analysis.DoesNotExist:
            raise NotFound()

    @method_decorator(
        permission_required("analyses.change_analysis", raise_exception=True)
    )
    def get(self, request, id, format=None):
        analysis = self.get_object(id)
        serializer = AnalysisSerializer(analysis)
        labs = LabSerializer(Lab.objects.all(), many=True)
        samples = SampleSerializer(
            Sample.objects.filter(Q(analysis__isnull=True) | Q(id=analysis.sample.id)),
            many=True,
        )
        users = UserSerializer(
            User.objects.filter(~Q(groups__name="používateľ")), many=True
        )
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
