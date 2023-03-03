from rest_framework.permissions import BasePermission


class SubjectViewPermission(BasePermission):
    def has_permission(self, request, view) -> bool:
        if view.action in ["create", "update", "destroy"]:
            return request.user.is_authenticated
        elif view.action in ["list_by_user"]:
            return True
        else:
            return False
