from apps.user.models import CustomUser
from apps.user.functions import CheckUser


class UserAuthentication(object):
    def authenticate(self, request, email=None, password=None):
        try:
            user = CustomUser.object.get(email=email)
            if user.check_password(password):
                return user
            return None
        except CustomUser.DoesNotExist:
            return None


    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None
