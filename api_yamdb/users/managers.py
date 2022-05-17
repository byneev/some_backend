from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, password, bio, email, role="user"):
        user = self.model(
            username=username,
            password=password,
            bio=bio,
            email=email,
            role=role,
        )
        user.save()
        return user

    def create_superuser(
        self, username, password, email, role="admin", bio=None
    ):
        user = self.model(
            username=username,
            password=password,
            bio=bio,
            email=email,
            role=role,
        )
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
