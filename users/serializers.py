from rest_framework import serializers
from .models import User, Role


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    name = serializers.ReadOnlyField()
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())

    def to_representation(self, instance):
        self.fields["role"] = RoleSerializer()
        return super(UserSerializer, self).to_representation(instance)


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"
