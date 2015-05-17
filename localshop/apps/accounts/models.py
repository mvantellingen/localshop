from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _
from model_utils.models import TimeStampedModel


@python_2_unicode_compatible
class Team(TimeStampedModel):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500, blank=True)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through='TeamMember')

    def __str__(self):
        return self.name

    def owners(self):
        return [member.user for member in self.members.filter(role='owner')]


class TeamMember(TimeStampedModel):
    team = models.ForeignKey(Team, related_name='members')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    role = models.CharField(max_length=100, choices=[
        ('owner', _("Owner")),
        ('developer', _("Developer")),
    ])

    class Meta:
        unique_together = [
            ('team', 'user'),
        ]
