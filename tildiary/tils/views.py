from json import JSONDecodeError
from typing import Any, Optional, Type

from django.db import transaction
from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.serializers import BaseSerializer

from subjects.models import Subject
from tags.models import Tag
from tils.models import Til
from tils.permissions import TilViewPermission
from tils.serializers import (DetailTilSerializer, ListTilSerializer,
                              PostTilSerializer)


class TilViewSet(viewsets.GenericViewSet):
    queryset = Til.objects.prefetch_related("tags").all()
    serializer_class = PostTilSerializer
    permission_classes = (TilViewPermission,)

    def get_serializer_class(self) -> Type[BaseSerializer[Any]]:
        if self.action == "create" or self.action == "update":
            return PostTilSerializer
        if self.action == "list_by_user" or self.action == "list_by_subject":
            return ListTilSerializer
        if self.action == "retrieve":
            return DetailTilSerializer
        return super().get_serializer_class()

    @transaction.atomic
    def create(self, request: Request) -> HttpResponse:
        data = request.data.copy()
        data['author'] = request.user.id

        serializer = self.get_serializer(
            data=data,
            context={'user': request.user},
        )
        serializer.is_valid(raise_exception=True)
        til: Til = serializer.save()

        try:
            tags: list = request.data['tags']
        except (KeyError, JSONDecodeError):
            tags = []

        tag_objects = [Tag(tag=tag, til=til) for tag in tags]

        Tag.objects.bulk_create(tag_objects)

        return JsonResponse(data=serializer.data, status=201)

    def retrieve(
        self,
        request: Request,
        pk: Optional[int] = None
    ) -> HttpResponse:
        try:
            til = self.get_queryset().get(id=pk)
        except Til.DoesNotExist:
            return HttpResponse("Not Found", status=404)

        if til.author.id != request.user.id and not til.is_opened:
            return HttpResponse("Not Found", status=404)

        serializer = self.get_serializer(instance=til)
        return JsonResponse(serializer.data, status=200, safe=False)

    @action(
        detail=False,
        methods=["get"],
        url_path=r"users/(?P<user_id>\d+)"
    )
    def list_by_user(self, request: Request, user_id: int) -> HttpResponse:
        til_list = self.get_queryset().filter(author__id=user_id)
        print(user_id, request.user.id)
        if user_id != request.user.id:
            til_list = til_list.filter(is_opened=True)

        serializer = self.get_serializer(
            instance=til_list, many=True
        )
        return JsonResponse(serializer.data, status=200, safe=False)

    @action(
        detail=False,
        methods=["get"],
        url_path=r"subjects/(?P<subject_id>\d+)"
    )
    def list_by_subject(
        self,
        request: Request,
        subject_id: int
    ) -> HttpResponse:
        til_list = self.get_queryset().filter(subject=subject_id)

        try:
            subject = Subject.objects.all().get(id=subject_id)
        except Subject.DoesNotExist:
            return HttpResponse("Not Found", status=404)

        if subject.author.id != request.user.id:
            til_list = til_list.filter(is_opened=True)

        serializer = self.get_serializer(
            instance=til_list, many=True
        )
        return JsonResponse(serializer.data, status=200, safe=False)

    def update(
        self,
        request: Request,
        pk: Optional[int] = None
    ) -> HttpResponse:
        # TODO: Authentication
        try:
            til = self.get_queryset().get(id=pk)
        except Subject.DoesNotExist:
            return HttpResponse("Not Found", status=404)

        if til.author.id != request.user.id:
            return HttpResponse("Not owned til", status=401)

        serializer = self.get_serializer(
            instance=til, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=200, safe=False)

    def destroy(
        self,
        request: Request,
        pk: Optional[int] = None
    ) -> HttpResponse:
        # TODO: Authentication
        try:
            til = self.get_queryset().get(id=pk)
        except Subject.DoesNotExist:
            return HttpResponse("Not Found", status=404)

        if til.author.id != request.user.id:
            return HttpResponse("Not owned til", status=401)

        til.delete()
        return HttpResponse(status=204)
