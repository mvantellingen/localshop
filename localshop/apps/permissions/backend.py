from django.contrib.auth.backends import ModelBackend

from .models import Credential


class CredentialBackend(ModelBackend):
    def authenticate(self, access_key=None, secret_key=None):
        try:
            credential = Credential.objects.active().get(access_key=access_key,
                                                         secret_key=secret_key)
        except (Credential.DoesNotExist,
                Credential.MultipleObjectsReturned):
            pass
        else:
            if credential.creator.is_active:
                return credential.creator
        return None
