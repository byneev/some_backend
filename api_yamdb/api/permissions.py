from rest_framework import permissions


class OwnerGetPatchPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method == "GET" or request.method == "PATCH"
        ) and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return request.user.username == obj.username


class GTEAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role != "user" and request.user.is_authenticated


class OnlyPost(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method == "POST"
