from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action

from subjects.models import Subject
from subjects.permissions import SubjectViewPermission
from subjects.serializers import SubjectSerializer


class SubjectViewSet(viewsets.GenericViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = (SubjectViewPermission,)

    def create(self, request):
        data = request.data.copy()
        data['author'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(data=serializer.data, status=201)

    @action(
        detail=False,
        methods=["get"],
        url_path=r"users/(?P<user_id>\d+)"
    )
    def list_by_user(self, request, user_id):
        subject_list = self.get_queryset().filter(author__id=user_id)

        if user_id != request.user.id:
            subject_list = subject_list.filter(is_opened=True)

        serializer = self.get_serializer(
            instance=subject_list, many=True
        )
        return JsonResponse(serializer.data, status=200, safe=False)

    def update(self, request, pk=None):
        try:
            subject = self.get_queryset().get(id=pk)
        except Subject.DoesNotExist:
            return HttpResponse("Not Found", status=404)

        if subject.author.id != request.user.id:
            return HttpResponse("Not owned subject", status=401)

        serializer = self.get_serializer(
            instance=subject, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(serializer.data, status=200, safe=False)

    def destroy(self, request, pk=None):
        try:
            subject = self.get_queryset().get(id=pk)
        except Subject.DoesNotExist:
            return HttpResponse("Not Found", status=404)

        if subject.author.id != request.user.id:
            return HttpResponse("Not owned til", status=401)

        subject.delete()
        return HttpResponse(status=204)
