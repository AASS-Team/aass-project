from rest_framework import serializers
from .models import Sample, User
from grants.models import Grant
from labs.models import Lab
from tools.models import Tool


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    name = serializers.ReadOnlyField()


class GrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grant
        fields = "__all__"


class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sample
        fields = "__all__"

    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    grant = serializers.PrimaryKeyRelatedField(
        queryset=Grant.objects.all(), required=False
    )

    def to_representation(self, instance):
        self.fields["user"] = UserSerializer()
        self.fields["grant"] = GrantSerializer()
        return super(SampleSerializer, self).to_representation(instance)


class LabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lab
        fields = "__all__"


class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = "__all__"
