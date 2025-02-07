from rest_framework import permissions

class CheckStudent(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.role == 'student'

class CheckTeacher(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.role == 'teacher'