import netaddr

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _
from userena.models import UserenaBaseProfile
from uuidfield import UUIDField

from localshop.utils import now


class AuthProfile(UserenaBaseProfile):
    user = models.OneToOneField(
        User, unique=True, verbose_name=_('user'), related_name='auth_profile')


class CIDRManager(models.Manager):
    def has_access(self, ip_addr, with_credentials=True):
        cidrs = self.filter(
            require_credentials=with_credentials
        ).values_list('cidr', flat=True)
        return bool(netaddr.all_matching_cidrs(ip_addr, cidrs))


class CIDR(models.Model):
    cidr = models.CharField('CIDR', max_length=128, unique=True,
        help_text='IP addresses and/or subnet')
    label = models.CharField('label', max_length=128, blank=True, null=True,
        help_text='Human-readable name (optional)')
    require_credentials = models.BooleanField(default=True)

    objects = CIDRManager()

    def __unicode__(self):
        return self.cidr

    class Meta:
        permissions = (
            ("view_cidr", "Can view CIDR"),
        )


class CredentialManager(models.Manager):

    def active(self):
        return self.filter(deactivated__isnull=True)


class Credential(models.Model):
    access_key = UUIDField(verbose_name='Access key', help_text='The access key', auto=True, db_index=True)
    secret_key = UUIDField(verbose_name='Secret key', help_text='The secret key', auto=True, db_index=True)
    creator = models.ForeignKey(User)
    created = models.DateTimeField(default=now)
    deactivated = models.DateTimeField(blank=True, null=True)
    comment = models.CharField(max_length=255, blank=True, null=True, default='',
        help_text="A comment about this credential, e.g. where it's being used")

    objects = CredentialManager()

    def __unicode__(self):
        return self.access_key.hex

    class Meta:
        ordering = ['-created']
        permissions = (
            ("view_credential", "Can view credential"),
        )
