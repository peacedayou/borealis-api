from rest_framework.permissions import IsAuthenticated

class IsAdminOrReadOnly(IsAuthenticated):
    def has_permission(self, request, view):
        return request.user.is_staff or request.method in ['GET']
