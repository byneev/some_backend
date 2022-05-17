from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.db.models import Sum


def get_average_score(title):
    reviews = Review.objects.filter(title=title)
    if not len(reviews):
        return 0
    sum_of_scores = reviews.aggregate(Sum("score"))
    average_score = int(sum_of_scores["score__sum"] / len(reviews))
    return average_score


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

    def validate(self, data):
        if self.context.get("request").method == "PATCH":
            return data
        user = self.context.get("request").user
        title_id = self.context.get("view").kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        reviews = Review.objects.filter(title=title)
        for item in reviews:
            if item.author.username == user.username:
                raise serializers.ValidationError(
                    "User can write only one review for each title"
                )
        return data


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


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field="slug", read_only=True, many=True
    )
    category = serializers.SlugRelatedField(slug_field="slug", read_only=True)
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        return get_average_score(obj)

    class Meta:
        model = Title
        fields = (
            "id",
            "name",
            "year",
            "description",
            "genre",
            "category",
            "rating",
        )


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name", "slug")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name", "slug")
