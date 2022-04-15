from rest_framework import serializers
from samples.models import Grant


class GrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grant
        fields = (
            "id",
            "name",
            "samples",
        )
        read_only_fields = (
            "samples",
        )  # read only when saving grant, so samples won't be NULL after save
