from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    ReviewViewSet,
    SignUpView,
    TitleViewSet,
    TokenView,
    UserMyselfView,
    UsersViewSet,
    CommentViewSet,
)


API_VERSION = "api/v1/"

router = DefaultRouter()
router.register("auth/signup", SignUpView)
router.register("users", UsersViewSet)
router.register(
    r"titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments",
    CommentViewSet,
    basename="comment",
)
router.register(
    r"titles/(?P<title_id>\d+)/reviews",
    ReviewViewSet,
    basename="review",
)
router.register("titles", TitleViewSet, basename="title")

urlpatterns = [
    path(
        "auth/token/",
        TokenView.as_view(),
        name="token",
    ),
    path("users/me/", UserMyselfView.as_view(), name="users/me"),
    path("", include(router.urls)),
]
