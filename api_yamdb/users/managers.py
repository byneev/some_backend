from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email):
        user = self.model(username=username, email=email, role="user")
        user.save()
        return user

    def create_superuser(self, username, password, email=None):
        user = self.model(username=username, email=email, role="admin")
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
