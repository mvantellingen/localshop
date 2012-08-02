from django.contrib.auth.backends import ModelBackend

from .models import Credential


class CredentialBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        try:
            credential = Credential.objects.active().get(access_key=username,
                                                         secret_key=password)
        except (Credential.DoesNotExist,
                Credential.MultipleObjectsReturned):
            pass
        else:
            if credential.creator.is_active:
                return credential.creator
        return None
