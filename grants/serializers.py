from rest_framework import serializers
from app.models import Grant
from app.models import Lab, User, Sample
from app.serializers import SampleSerializer, LabSerializer, UserSerializer


class GrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grant
        fields = "__all__"

    # sample = serializers.PrimaryKeyRelatedField(queryset=Sample.objects.all())
    # lab = serializers.PrimaryKeyRelatedField(queryset=Lab.objects.all())
    # laborant = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    # # tools = serializers.PrimaryKeyRelatedField(queryset=Tool.objects.all(), many=True)
    #
    # def to_representation(self, instance):
    #     self.fields["sample"] = SampleSerializer()
    #     self.fields["lab"] = LabSerializer()
    #     self.fields["laborant"] = UserSerializer()
    #     # self.fields["tools"] = ToolSerializer()
    #
    #     return super(AnalysisSerializer, self).to_representation(instance)
