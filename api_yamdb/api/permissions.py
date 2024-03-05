from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsSuperUserOrOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.role == 'moderator'
            or request.user.role == 'admin'
            or request.user.is_superuser
            or obj.author == request.user
        )


class IsSuperUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return request.method in SAFE_METHODS
        return request.user.role == 'admin'

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.role == 'moderator'
            or request.user.role == 'admin'
        )


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.role == 'admin'
