from os import truncate
from rest_framework.permissions import SAFE_METHODS, BasePermission


class EditPermission(BasePermission):
    message = 'Editing questions is restricted to the author only.'

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        return obj.user == request.user


class UserEditPermission(BasePermission):

    def has_object_permission(self, request, view, obj):

        if request.method in ('HEAD', 'OPTIONS'):
            return True

        return obj.htno == request.user.htno
