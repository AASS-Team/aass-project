from rest_framework import serializers

from .models import Analysis
from samples.models import Sample
from samples.serializers import SampleSerializer
from users.models import User
from users.serializers import UserSerializer
from labs.models import Lab
from labs.serializers import LabSerializer
from tools.models import Tool
from tools.serializers import ToolSerializer


class AnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analysis
        fields = "__all__"

    sample = serializers.PrimaryKeyRelatedField(queryset=Sample.objects.all())
    lab = serializers.PrimaryKeyRelatedField(queryset=Lab.objects.all())
    laborant = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    tools = serializers.PrimaryKeyRelatedField(queryset=Tool.objects.all(), many=True)
    status = serializers.ReadOnlyField()
    started_at = serializers.DateTimeField(required=False)
    ended_at = serializers.DateTimeField(required=False)

    def to_representation(self, instance):
        self.fields["sample"] = SampleSerializer()
        self.fields["lab"] = LabSerializer()
        self.fields["laborant"] = UserSerializer()
        self.fields["tools"] = ToolSerializer(many=True)

        return super(AnalysisSerializer, self).to_representation(instance)
