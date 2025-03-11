from rest_framework.permissions import BasePermission
from rest_framework import permissions


class ProfilePermission(BasePermission) :
       def has_object_permission(self, request, view, obj):
              request.user = obj.user

class PrivateGroupPermission(BasePermission) :
       def has_object_permission(self, request, view, obj):
              request.user.accounts in obj.memebers.all() and request.user.is_athenticated

class PermissionToUpdatePrivateGroup(BasePermission) : 
    def has_object_permission(self, request, view, obj):
       return obj.owner == request.user.accounts      

class PermissionModifyComment(BasePermission) : 
    def has_object_permission(self, request, view, obj):
       return obj.owner == request.user.accounts