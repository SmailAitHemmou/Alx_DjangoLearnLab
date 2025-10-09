from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Safe methods allowed for everyone. Non-safe methods only if request.user == obj.author.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return getattr(obj, 'author', None) == request.user
