from django.contrib.auth.base_user import BaseUserManager

USER = 1
SUPERUSER = 4


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self):
        user = self.model(role=USER)
        user.save()
        return user

    def create_superuser(self, username, password, email=None):
        user = self.model(username=username, email=email, role=SUPERUSER)
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user
