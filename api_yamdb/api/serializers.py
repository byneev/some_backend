from django.shortcuts import get_object_or_404
from rest_framework import serializers
from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")


class TokenSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password"].required = False
        self.fields["confirmation_code"] = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get("username", None)
        confirmation_code = attrs.get("confirmation_code", None)
        real_user = get_object_or_404(User, username=username)

        if not real_user.confirmation_code == confirmation_code:
            raise KeyError("Not correct confirmation code")

        data = {}
        refresh = self.get_token(real_user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data
