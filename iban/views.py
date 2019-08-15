from rest_framework import viewsets

from .models import IBAN
from .serializers import IBANSerializer


class IBANViewSet(viewsets.ModelViewSet):
    queryset = IBAN.objects.all()
    serializer_class = IBANSerializer
