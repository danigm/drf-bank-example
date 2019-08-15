from rest_framework import viewsets
from rest_framework.permissions import BasePermission

from .models import IBAN
from .serializers import IBANSerializer


class AdminCreatorOnlyPermission(BasePermission):

    def has_permission(self, request, viewset):
        if not request.user or not request.user.is_authenticated:
            return False

        if not request.user.is_superuser:
            return False

        # Restrict manipulation operations on a user to the administrator who
        # created them
        if viewset.get_object().creator == request.user:
            return True

        return False


class IBANViewSet(viewsets.ModelViewSet):
    queryset = IBAN.objects.all()
    serializer_class = IBANSerializer

    def get_permissions(self):
        if self.action in ['partial_update', 'update', 'destroy']:
            return [AdminCreatorOnlyPermission()]

        return super().get_permissions()
