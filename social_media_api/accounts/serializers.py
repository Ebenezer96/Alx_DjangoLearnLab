from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "bio",
            "profile_picture",
        )

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"],
            bio=validated_data.get("bio", ""),
            profile_picture=validated_data.get("profile_picture"),
        )
        Token.objects.create(user=user)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            username=data.get("username"),
            password=data.get("password"),
        )
        if not user:
            raise serializers.ValidationError("Invalid credentials")

        token, _ = Token.objects.get_or_create(user=user)
        return {
            "user": user,
            "token": token.key,
        }


class UserProfileSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(
        source="followers.count", read_only=True
    )
    following_count = serializers.IntegerField(
        source="following.count", read_only=True
    )

    class Meta:
        model = User
