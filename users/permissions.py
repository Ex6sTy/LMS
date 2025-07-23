from rest_framework.permissions import BasePermission
from users.models import Payment


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderators").exists()


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsSelf(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsOwnerOrModer(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            obj.user == request.user
            or request.user.groups.filter(name="Модератор").exists()
        )


class HasPaidForCourse(BasePermission):
    def has_object_permission(self, request, view, obj):
        return Payment.objects.filter(user=request.user, paid_course=obj).exists()
