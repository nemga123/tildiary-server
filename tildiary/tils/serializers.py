from rest_framework import serializers

from subjects.models import Subject
from tils.models import Til


class PostTilSerializer(serializers.ModelSerializer):
    subject = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all(), many=False)
    
    class Meta:
        model = Til
        fields = "__all__"
