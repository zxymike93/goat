from accounts.models import Token, User


class PasswordlessAuthenticationBackend(object):

    def authenticate(self, uid):
        try:
            token = Token.objects.get(uid=uid)
            return User.objects.get(email=token.email)
        except User.DoesNotExist:
            return User.objects.create(email=token.email)
        except Token.DoesNotExist:
            return None

    def get_user(self, email):
        """
        得到已经认证过的user
        """
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        return user
