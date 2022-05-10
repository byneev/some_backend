from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import SignUpView, TokenView


API_VERSION = "api/v1/"

router = DefaultRouter()
router.register(API_VERSION + "auth/signup", SignUpView)


urlpatterns = [
    path("", include(router.urls)),
    path(
        API_VERSION + "auth/token/",
        TokenView.as_view(),
        name="token_view",
    ),
]
