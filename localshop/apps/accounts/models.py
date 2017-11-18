import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _
from model_utils.fields import AutoCreatedField
from model_utils.models import TimeStampedModel


class User(AbstractUser):
    pass


class AccessKey(models.Model):
    created = AutoCreatedField()

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='access_keys')

    access_key = models.UUIDField(
        verbose_name='Access key', help_text='The access key',
        default=uuid.uuid4, db_index=True)
    secret_key = models.UUIDField(
        verbose_name='Secret key', help_text='The secret key',
        default=uuid.uuid4, db_index=True)
    comment = models.CharField(
        max_length=255, blank=True, null=True, default='',
        help_text=_(
            "A comment about this credential, e.g. where it's being used"))
    last_usage = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created']


@python_2_unicode_compatible
class Team(TimeStampedModel):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500, blank=True)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through='TeamMember')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('accounts:team_detail', kwargs={'pk': self.pk})

    def owners(self):
        return [member.user for member in self.members.filter(role='owner')]


class TeamMember(TimeStampedModel):
    team = models.ForeignKey(Team, related_name='members')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='team_memberships')
    role = models.CharField(max_length=100, choices=[
        ('owner', _("Owner")),
        ('developer', _("Developer")),
    ])

    class Meta:
        unique_together = [
            ('team', 'user'),
        ]

    @property
    def is_owner(self):
        return self.role == 'owner'
