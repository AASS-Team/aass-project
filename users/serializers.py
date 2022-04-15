from django.contrib.auth.models import Group
from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "name",
            "first_name",
            "last_name",
            "email",
            "analyses",
            "samples",
            "groups",
        )
        read_only_fields = (
            "analyses",
            "samples",
        )  # read only when saving user, so analyses & samples won't be NULL after save

    def to_representation(self, instance):
        self.fields["groups"] = GroupSerializer(many=True)
        return super(UserSerializer, self).to_representation(instance)


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = (
            "id",
            "name",
        )
