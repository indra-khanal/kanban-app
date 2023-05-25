from django.shortcuts import get_object_or_404
from rest_framework import permissions
from django.contrib.auth.models import User
from core.models import KanBanBoard

class IsAdminUser(permissions.BasePermission):
	message = 'Permission Denied for current user'
	def has_permission(self, request, view):
		user = get_object_or_404(User, id = request.user.id)
		if user.is_active:
			return True
		return False


class IsBoardOwner(permissions.BasePermission):
    message = "You are not allowed to do current action"
    def has_permission(self, request, view):
        kanban_obj = get_object_or_404(KanBanBoard, id=view.kwargs.get("pk"))
        if kanban_obj.user.id == request.user.id:
            return True
        else:
            return False