from django.http import HttpRequest
from rest_framework.permissions import BasePermission
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet


class SubjectViewPermission(BasePermission):
    def has_permission(self, request: HttpRequest, view: APIView) -> bool:
        assert isinstance(view, GenericViewSet)

        if view.action in ["create", "update", "destroy"]:
            return request.user.is_authenticated
        elif view.action in ["list_by_user"]:
            return True
        else:
            return False
