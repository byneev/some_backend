from django.shortcuts import get_object_or_404
from rest_framework.viewsets import (
    ModelViewSet,
    ReadOnlyModelViewSet,
    GenericViewSet,
)
from django.db.models import Sum
from rest_framework.generics import RetrieveUpdateAPIView, mixins

from reviews.models import Review, Title
from .permissions import (
    GTEAdminPermission,
    GetAnyOrPostAuth,
    OnlyPost,
    OwnerGetPatchPermission,
    DeleteUpdateGTEAdminOrOwner,
)
from .serializers import (
    ReviewsSerializer,
    SignUpSerializer,
    TokenSerializer,
    UsersSerializer,
)
from users.models import User
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from api_yamdb.settings import EMAIL_HOST_USER
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions
from .exceptions import AlreadyExistException
from rest_framework.pagination import PageNumberPagination
from rest_framework import filters


class SignUpView(ModelViewSet):
    serializer_class = SignUpSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        isUserExist = User.objects.filter(
            username=self.request.data.get("username")
        ).exists()
        user = None
        if isUserExist:
            user = get_object_or_404(
                User, username=self.request.data.get("username")
            )
        if user and user.confirmation_code:
            raise AlreadyExistException()

        code = get_random_string(9)
        if user:
            if not user.email:
                raise KeyError("field Email doesnt exists in request")
            User.objects.filter(
                username=self.request.data.get("username")
            ).update(confirmation_code=code)
        else:
            serializer.save(confirmation_code=code, role="user")
        send_mail(
            "Yamdb confirmation code",
            f"There is your confirmation code to get token on Yamdb - {code}",
            EMAIL_HOST_USER,
            [self.request.data.get("email")],
            fail_silently=False,
        )


class TokenView(TokenObtainPairView):
    serializer_class = TokenSerializer
    permission_classes = (OnlyPost,)


class UserMyselfView(RetrieveUpdateAPIView):
    serializer_class = UsersSerializer
    permission_classes = (OwnerGetPatchPermission,)
    lookup_field = "me"

    def get_object(self):
        return get_object_or_404(User, username=self.request.user.username)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


class UsersViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (GTEAdminPermission,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ("username",)
    lookup_field = "username"


class GetPostReviewViewSet(ModelViewSet):
    serializer_class = ReviewsSerializer
    permission_classes = (GetAnyOrPostAuth,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title_id = self.kwargs.get("title_id")
        title = get_object_or_404(Title, id=title_id)
        return Review.objects.filter(title=title)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get("title_id"))
        print(title.rating)
        author = self.request.user
        serializer.save(title=title, author=author)
        reviews = Review.objects.filter(title=title)
        sum_of_scores = reviews.aggregate(Sum("score"))
        average_score = sum_of_scores["score__sum"] / len(reviews)
        print(average_score)
        title.rating = average_score
        title.save()


class PostDeleteUpdateReviewViewSet(
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    serializer_class = ReviewsSerializer
    permission_classes = (DeleteUpdateGTEAdminOrOwner,)

    def get_object(self):
        return get_object_or_404(Review, id=self.kwargs.get("reviews_id"))
