# from rest_framework.permissions import BasePermission


# class IsOwnerOrReadOnly(BasePermission):
#     """
#     Only the owner of a listing can update or delete it.
#     Read-only access is allowed for everyone.
#     """

#     def has_object_permission(self, request, view, obj):
#         # Allow read-only methods for everyone
#         if request.method in ('GET', 'HEAD', 'OPTIONS'):
#             return True

#         # Write permissions only for the owner
#         return obj.owner == request.user
    


from rest_framework.permissions import BasePermission, IsAuthenticated

class IsOwnerOrReadOnlyOrCanBuy(BasePermission):
    """
    Permissions:
    - Everyone can read (GET, HEAD, OPTIONS)
    - Owners can update/delete
    - Authenticated non-owners can 'buy'
    """

    def has_object_permission(self, request, view, obj):
        # Read-only for everyone
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True

        # Buy action allowed for authenticated non-owners
        if view.action == 'buy':
            return request.user.is_authenticated and obj.owner != request.user

        # Write permissions only for the owner
        return obj.owner == request.user