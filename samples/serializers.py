from rest_framework import serializers

from samples.models import Sample
from grants.serializers import GrantSerializer
from users.serializers import UserSerializer


class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sample
        fields = (
            "id",
            "name",
            "amount",
            "note",
            "user",
            "grant",
            "analysis",
        )
        read_only_fields = (
            "analysis",
        )  # read only when saving sample, so analysis won't be NULL after save

    def to_representation(self, instance):
        self.fields["user"] = UserSerializer()
        self.fields["grant"] = GrantSerializer()
        return super(SampleSerializer, self).to_representation(instance)
