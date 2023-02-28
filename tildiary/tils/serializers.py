from rest_framework import serializers

from subjects.models import Subject
from tils.models import Til


class PostTilSerializer(serializers.ModelSerializer):
    subject = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(), many=False
    )

    class Meta:
        model = Til
        fields = "__all__"


class ListTilSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Til
        fields = (
            "id",
            "title",
            "author",  # TODO: implement nested serializer
            "created_at",
            "tags",
        )

    def get_tags(self, obj):
        return [til_tag.tag.tag for til_tag in obj.tags.all()]


class DetailTilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Til
        fields = (
            "id",
            "title",
            "content",
            "author",
            "created_at",
            "tags",
        )

    def get_tags(self, obj):
        return [til_tag.tag.tag for til_tag in obj.tags.all()]
