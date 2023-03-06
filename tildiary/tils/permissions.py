from django.http import HttpRequest
from rest_framework.permissions import BasePermission
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet


class TilViewPermission(BasePermission):
    def has_permission(self, request: HttpRequest, view: APIView) -> bool:
        assert isinstance(view, ViewSet)

        if view.action in ["create", "update", "destroy"]:
            return request.user.is_authenticated
        elif view.action in ["list_by_user", "list_by_subject", "retrieve"]:
            return True
        else:
            return False
