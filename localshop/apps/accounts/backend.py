import uuid

from django.contrib.auth.backends import ModelBackend
from django.utils import timezone

from localshop.apps.accounts.models import AccessKey


class AccessKeyBackend(ModelBackend):
    def authenticate(self, access_key=None, secret_key=None):

        try:
            access_key = uuid.UUID(access_key)
            secret_key = uuid.UUID(secret_key)
            key = AccessKey.objects.get(
                access_key=access_key, secret_key=secret_key)
        except ValueError:
            pass
        except (AccessKey.DoesNotExist, AccessKey.MultipleObjectsReturned):
            pass
        else:
            if key.user.is_active:
                key.last_usage = timezone.now()
                key.save()
                return key.user

        return None
