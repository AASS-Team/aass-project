from rest_framework import serializers
from .models import Sample, User, Grant


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
