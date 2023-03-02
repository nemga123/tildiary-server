from rest_framework import serializers

from users.models import User


class AuthSignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=255)
    username = serializers.CharField(required=True, max_length=10)
    password = serializers.CharField(required=True)

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Duplicated email.")
        return email

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("Duplicated username.")
        return username

    def create(self, validated_data):
        username = validated_data.get("username")
        email = validated_data.get("email")
        password = validated_data.get("password")
        user = User.objects.create_user(
            username=username, email=email, password=password
        )

        return user
