from rest_framework import permissions


class OwnerGetPatchPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method == "GET" or request.method == "PATCH"
        ) and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        print("Hello")
        return request.user.username == obj.username
