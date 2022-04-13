from rest_framework import serializers
from app.models import Grant
from app.models import Lab, User, Sample
from app.serializers import SampleSerializer, LabSerializer, UserSerializer


class GrantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grant
        fields = "__all__"
