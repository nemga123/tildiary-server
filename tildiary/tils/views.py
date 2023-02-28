from django.http import HttpResponse, JsonResponse
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from tils.serializers import PostTilSerializer
from tils.models import Til


class TilViewSet(viewsets.GenericViewSet):
    queryset = Til.objects.all()
    serializer_class = PostTilSerializer
    permission_classes = (AllowAny,)

    # TODO: Authentication
    def create(self, request):
        serializer: PostTilSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return JsonResponse(data=serializer.data, status=201)
