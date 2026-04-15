
from users.models import User

class EmailBackend:
    def authenticate(self, request, username=None, email=None, password=None):
        email = email or username
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id: int):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None