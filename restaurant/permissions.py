from rest_framework.permissions import BasePermission


class IsManagerUser(BasePermission):
    def has_permission(self, request, view):
        return isManager(request)


class IsCustomerUser(BasePermission):
    def has_permission(self, request, view): 
        return bool(
            request.user and
            request.user.is_authenticated and
            not isManager(request) and 
            not isCrew(request)
        )

        
class IsDeliveryCrewUser(BasePermission):
    def has_permission(self, request, view):
        return isCrew(request)


class IsManagerorCrewUser(BasePermission):
    def has_permission(self, request, view):
        return bool(
            isManager(request)
            or isCrew(request)
        )


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


def isManager(request): 
    return bool(
        request.user
        and request.user.is_authenticated
        and request.user.groups.filter(name='Manager').exists()
    )


def isCrew(request):
    return bool(
        request.user
        and request.user.is_authenticated
        and request.user.groups.filter(name='Delivery crew').exists()
    )
