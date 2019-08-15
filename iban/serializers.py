from rest_framework import serializers
from .models import IBAN, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class IBANSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = IBAN
        fields = ['user', 'number']



