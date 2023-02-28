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

    def get_tags(self, obj) -> list:
        return [tag.tag for tag in obj.tags.all()]


class DetailTilSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField()

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

    def get_tags(self, obj) -> list:
        print(obj.tags.all())
        return [tag.tag for tag in obj.tags.all()]
