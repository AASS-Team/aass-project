from django.contrib.auth.models import Group
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    name = serializers.ReadOnlyField()
    groups = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=True)

    def to_representation(self, instance):
        self.fields["groups"] = GroupSerializer(many=True)
        return super(UserSerializer, self).to_representation(instance)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "name"]
