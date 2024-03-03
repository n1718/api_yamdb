from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user


class IsSuperUserOrOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or request.user.role == 'moderator'
            or request.user.role == 'admin'
        )


class IsSuperUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # return (
        #     request.method in SAFE_METHODS
        #     or request.user.is_authenticated
        # )
        if not request.user.is_authenticated:
            return request.method in SAFE_METHODS
        return (request.user.role == 'admin'
                or request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.role == 'moderator'
            or request.user.role == 'admin'
        )
