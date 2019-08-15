from uuid import uuid4

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

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        random_username = str(uuid4())
        user = User.objects.create(username=random_username, **user_data)
        return IBAN.objects.create(user=user, **validated_data)

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        user = instance.user

        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)

        instance.number = validated_data.get('number', instance.number)

        return instance
