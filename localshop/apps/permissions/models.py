import uuid
import netaddr

from django.db import models
from django.utils.translation import ugettext as _
from model_utils.fields import AutoCreatedField


class CIDRManager(models.Manager):
    def has_access(self, ip_addr, with_credentials=True):
        cidrs = self.filter(
            require_credentials=with_credentials
        ).values_list('cidr', flat=True)
        return bool(netaddr.all_matching_cidrs(ip_addr, cidrs))


class CIDR(models.Model):
    """Allow access based on the IP address of the client."""
    repository = models.ForeignKey(
        'packages.Repository', related_name='cidr_list')
    cidr = models.CharField(
        'CIDR', max_length=128, help_text='IP addresses and/or subnet')
    label = models.CharField(
        'label', max_length=128, blank=True, null=True,
        help_text='Human-readable name (optional)')
    require_credentials = models.BooleanField(default=True)

    objects = CIDRManager()

    def __unicode__(self):
        return self.cidr

    class Meta:
        unique_together = [
            ('repository', 'cidr'),
        ]
        permissions = (
            ("view_cidr", "Can view CIDR"),
        )


class CredentialManager(models.Manager):

    def active(self):
        return self.filter(deactivated__isnull=True)

    def authenticate(self, key, secret):
        try:
            key = uuid.UUID(key)
            secret = uuid.UUID(secret)
        except ValueError:
            return self.none()
        else:
            return self.active().filter(access_key=key, secret_key=secret).first()


class Credential(models.Model):
    """Credentials are repository bound"""
    created = AutoCreatedField()

    repository = models.ForeignKey('packages.Repository', related_name='credentials')
    access_key = models.UUIDField(verbose_name='Access key', help_text='The access key', default=uuid.uuid4, db_index=True)
    secret_key = models.UUIDField(verbose_name='Secret key', help_text='The secret key', default=uuid.uuid4, db_index=True)
    comment = models.CharField(
        max_length=255, blank=True, null=True, default='',
        help_text="A comment about this credential, e.g. where it's being used")

    allow_upload = models.BooleanField(
        default=True,
        help_text=_("Indicate if these credentials allow uploading new files"))
    deactivated = models.DateTimeField(blank=True, null=True)

    objects = CredentialManager()

    def __unicode__(self):
        return self.access_key.hex

    class Meta:
        ordering = ['-created']
        permissions = (
            ("view_credential", "Can view credential"),
        )

