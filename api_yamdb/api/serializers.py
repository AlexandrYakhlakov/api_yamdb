from rest_framework import serializers
from reviews.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        model = User


class SendConfirmCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')