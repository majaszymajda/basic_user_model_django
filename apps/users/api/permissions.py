from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.pk == request.user.id


class IsOwnerOrIsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        if request.user.is_staff:
            return True

        return obj.user.pk == request.user.pk
