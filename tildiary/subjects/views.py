from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from subjects.models import Subject
from subjects.serializers import SubjectSerializer


class SubjectViewSet(viewsets.GenericViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = (AllowAny,)

    def create(self, request):
        serializer: SubjectSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(data=serializer.data, status=201)

    def list(self, request):
        user_id = request.GET.get("user", None)
        subject_list = self.get_queryset().filter(author=user_id)
        serializer: SubjectSerializer = self.get_serializer(
            instance=subject_list, many=True
        )
        return JsonResponse(serializer.data, status=200, safe=False)

    def update(self, request, pk=None):
        # TODO: Authentication
        try:
            subject = self.get_queryset().get(id=pk)
        except Subject.DoesNotExist:
            return HttpResponse("Not Found", status=404)
        serializer: SubjectSerializer = self.get_serializer(
            instance=subject, data=request.data, partial=True
        )
        serializer.is_valid()
        serializer.save()
        return JsonResponse(serializer.data, status=200, safe=False)

    def destroy(self, request, pk=None):
        # TODO: Authentication
        try:
            subject = self.get_queryset().get(id=pk)
        except Subject.DoesNotExist:
            return HttpResponse("Not Found", status=404)
        subject.delete()
        return HttpResponse(status=204)
