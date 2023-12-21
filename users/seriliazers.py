from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "telegram_id",
            "phone",
            "city",
            "avatar",
            "role",
            "first_name",
            "last_name",
            "is_active",
            "password"
        )


