from rest_framework import serializers
from samples.models import Grant


class GrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grant
        fields = "__all__"
