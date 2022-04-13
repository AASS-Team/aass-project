from rest_framework import serializers

from samples.models import Sample, User
from grants.models import Grant
from grants.serializers import GrantSerializer
from users.serializers import UserSerializer


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
