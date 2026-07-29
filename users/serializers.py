
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model  = CustomUser
        fields = ["email", "password", "role"]

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email    = validated_data["email"],
            password = validated_data["password"],
            role     = validated_data["role"],
        )
        return user
    

class LoginSerializer(serializers.Serializer):

    email    = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid credentials")

        # Generate tokens
        refresh = RefreshToken.for_user(user)

        return {
            "user": user,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "role": user.role
        }
