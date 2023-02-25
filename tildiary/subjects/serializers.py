from rest_framework import serializers

from subjects.models import Subject


class SubjectSerializer(serializers.ModelSerializer):
    til_counts = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = "__all__"
        read_only_fields = ("id", "til_counts")

    def get_til_counts(self, obj: Subject) -> int:
        return obj.tils.count()
