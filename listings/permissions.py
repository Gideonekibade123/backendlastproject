# from rest_framework.permissions import BasePermission, IsAuthenticated

# class IsOwnerOrReadOnlyOrCanBuy(BasePermission):
#     """
#     Permissions:
#     - Everyone can read (GET, HEAD, OPTIONS)
#     - Owners can update/delete
#     - Authenticated non-owners can 'buy'
#     """

#     def has_object_permission(self, request, view, obj):
#         # Read-only for everyone
#         if request.method in ('GET', 'HEAD', 'OPTIONS'):
#             return True

#         # Buy action allowed for authenticated non-owners
#         if view.action == 'buy':
#             return request.user.is_authenticated and obj.owner != request.user

#         # Write permissions only for the owner
#         return obj.owner == request.user
    



from rest_framework.permissions import BasePermission

class IsOwnerOrReadOnlyOrCanBuy(BasePermission):
    """
    Permissions:
    - Everyone can read (GET, HEAD, OPTIONS)
    - Owners can update/delete
    - Authenticated non-owners can 'buy' via a dedicated buy endpoint
    """

    def has_object_permission(self, request, view, obj):
        # Everyone can read
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True

        # Buy action: mark buy endpoint with a custom attribute on the view
        if getattr(view, 'buy_action', False):
            return request.user.is_authenticated and obj.owner != request.user

        # Write permissions only for the owner
        return obj.owner == request.user
