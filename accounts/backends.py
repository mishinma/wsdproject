from django.contrib.auth import backends
from accounts.models import UserMethods


class ModelBackend(backends.ModelBackend):

    def get_user(self, user_id):
        try:
            return UserMethods.objects.get(pk=user_id)
        except UserMethods.DoesNotExist:
            return None
