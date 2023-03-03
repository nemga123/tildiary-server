from rest_framework.permissions import BasePermission


class TilViewPermission(BasePermission):
    def has_permission(self, request, view) -> bool:
        if view.action in ["create", "update", "destroy"]:
            return request.user.is_authenticated
        elif view.action in ["list_by_user", "list_by_subject", "retrieve"]:
            return True
        else:
            return False
