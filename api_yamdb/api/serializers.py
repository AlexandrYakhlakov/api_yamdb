from rest_framework import serializers
from django.contrib.auth.validators import UnicodeUsernameValidator
from reviews.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        model = User


class AuthSignupSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254, required=True)
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=(UnicodeUsernameValidator(),)
    )

    def validate_username(self, username):
        if username == 'me':
            raise serializers.ValidationError('Недопустимое имя для логина')
        return username





class GetTokenSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField(required=True)
    username = serializers.CharField(required=True)