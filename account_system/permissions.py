from rest_framework import permissions
from account_system.models import UserAccount

class ViewOnlyPermission(permissions.BasePermission):
    """
    Custom permission to allow only view (GET) access for users with 'view_only' access to the account.
    """

    def has_permission(self, request, view):
        # Allow safe methods (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Retrieve the account from the view's kwargs (account_pk)
        account_id = view.kwargs.get('account_pk')
        if not account_id:
            return False

        # Check if the user has 'view_only' access to this account
        try:
            user_account = UserAccount.objects.get(user=request.user, account_id=account_id)
            if user_account.account_type == 'view_only':
                # Only allow read access, deny anything else
                return request.method in permissions.SAFE_METHODS
        except UserAccount.DoesNotExist:
            return False

        return False

class FullAccessPermission(permissions.BasePermission):
    """
    Custom permission to allow full CRUD access for users with 'full_access' to the account.
    """

    def has_permission(self, request, view):
        # Check if the account_id is in the URL
        account_id = view.kwargs.get('account_pk')
        if not account_id:
            return False

        try:
            user_account = UserAccount.objects.get(user=request.user, account_id=account_id)
            if user_account.account_type == 'full_access':
                # Allow all methods (full CRUD access)
                return True
            
            # Default to ViewOnlyPermission if not full_access
            return ViewOnlyPermission().has_permission(request, view)
        except UserAccount.DoesNotExist:
            return False
        

class PostOnlyPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user and request.user.is_authenticated
        return False    
