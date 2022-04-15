from rest_framework import serializers

from tools.models import Tool


class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = (
            "id",
            "name",
            "type",
            "available",
            "analysis",
        )
        read_only_fields = (
            "analysis",
        )  # read only when saving tool, so analysis won't be NULL after save

    available = serializers.ReadOnlyField()
