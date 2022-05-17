from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import Comment, Review, Title
from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email")
        extra_kwargs = {"username": {"validators": []}}


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
            raise serializers.ValidationError("Not correct confirmation code")

        data = {}
        refresh = self.get_token(real_user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data


class UsersMyselfSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "role",
        )


class ReviewsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        model = Review
        fields = (
            "id",
            "text",
            "author",
            "score",
            "pub_date",
        )


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field="username", read_only=True
    )

    class Meta:
        model = Comment
        fields = (
            "id",
            "text",
            "author",
            "pub_date",
        )


class TitlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = (
            "name",
            "year",
            "description",
            "genre",
            "category"
        )
