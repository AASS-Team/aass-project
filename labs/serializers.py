from rest_framework import serializers

from labs.models import Lab


class LabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab
        fields = (
            "id",
            "name",
            "address",
            "available",
            "analysis",
        )
        read_only_fields = (
            "analysis",
        )  # read only when saving lab, so analysis won't be NULL after save

    available = serializers.ReadOnlyField()
