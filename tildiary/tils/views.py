from json import JSONDecodeError

from django.db import transaction
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from subjects.models import Subject
from tags.models import Tag
from tils.models import Til
from tils.serializers import (DetailTilSerializer, ListTilSerializer,
                              PostTilSerializer)


class TilViewSet(viewsets.GenericViewSet):
    queryset = Til.objects.prefetch_related("tags").all()
    serializer_class = PostTilSerializer
    permission_classes = (AllowAny,)

    def get_serializer_class(self):
        if self.action == "create" or self.action == "update":
            return PostTilSerializer
        if self.action == "list_by_user" or self.action == "list_by_subject":
            return ListTilSerializer
        if self.action == "retrieve":
            return DetailTilSerializer
        return super().get_serializer_class()

    # TODO: Authentication
    @transaction.atomic
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        til: Til = serializer.save()

        try:
            tags: list = request.data['tags']
        except (KeyError, JSONDecodeError):
            tags = []

        tag_objects = [Tag(tag=tag, til=til) for tag in tags]

        Tag.objects.bulk_create(tag_objects)

        return JsonResponse(data=serializer.data, status=201)

    def retrieve(self, request, pk=None):
        try:
            til = self.get_queryset().get(id=pk)
        except Til.DoesNotExist:
            return HttpResponse("Not Found", status=404)

        if til.author != request.user.id and not til.is_opened:
            return HttpResponse("Not Found", status=404)

        serializer = self.get_serializer(instance=til)
        return JsonResponse(serializer.data, status=200, safe=False)

    @action(
        detail=False,
        methods=["get"],
        url_path=r"users/(?P<user_id>\d+)"
    )
    def list_by_user(self, request, user_id):
        til_list = self.get_queryset().filter(author=user_id)

        if user_id != request.user.id:
            til_list.filter(is_opened=True)

        serializer = self.get_serializer(
            instance=til_list, many=True
        )
        return JsonResponse(serializer.data, status=200, safe=False)

    @action(
        detail=False,
        methods=["get"],
        url_path=r"subjects/(?P<subject_id>\d+)"
    )
    def list_by_subject(self, request, subject_id):
        til_list = self.get_queryset().filter(subject=subject_id)

        try:
            subject = Subject.objects.all().get(id=subject_id)
        except Subject.DoesNotExist:
            return HttpResponse("Not Found", status=404)

        if subject.author != request.user.id:
            til_list.filter(is_opened=True)

        serializer = self.get_serializer(
            instance=til_list, many=True
        )
        return JsonResponse(serializer.data, status=200, safe=False)

    def update(self, request, pk=None):
        # TODO: Authentication
        try:
            til = self.get_queryset().get(id=pk)
        except Subject.DoesNotExist:
            return HttpResponse("Not Found", status=404)
        serializer = self.get_serializer(
            instance=til, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=200, safe=False)

    def destroy(self, request, pk=None):
        # TODO: Authentication
        try:
            til = self.get_queryset().get(id=pk)
        except Subject.DoesNotExist:
            return HttpResponse("Not Found", status=404)
        til.delete()
        return HttpResponse(status=204)
