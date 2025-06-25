from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from users.models import CustomUser, Payment

User = get_user_model()


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "phone",
            "city",
            "avatar",
            "payments",
        )


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["id", "email", "username", "password"]

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "country", "phone")


class PrivateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ("password",)
