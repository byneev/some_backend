from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveAPIView
from .permissions import OwnerGetPatchPermission
from .serializers import (
    SignUpSerializer,
    TokenSerializer,
    UsersMyselfSerializer,
)
from users.models import SIMPLE_USER, User
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from api_yamdb.settings import EMAIL_HOST_USER
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import permissions
from .exceptions import AlreadyExistException


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
            serializer.save(confirmation_code=code, role=SIMPLE_USER)
        send_mail(
            "Yamdb confirmation code",
            f"There is your confirmation code to get token on Yamdb - {code}",
            EMAIL_HOST_USER,
            [self.request.data.get("email")],
            fail_silently=False,
        )


class TokenView(TokenObtainPairView):
    serializer_class = TokenSerializer
    permission_classes = (permissions.AllowAny,)


class UsersMyselfView(ModelViewSet):
    serializer_class = UsersMyselfSerializer
    permission_classes = (OwnerGetPatchPermission,)

    def get_queryset(self):
        return User.objects.filter(username=self.request.user.username)
