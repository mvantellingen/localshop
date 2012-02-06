import netaddr
from django.db import models


class Manager(models.Manager):
    def has_access(self, ip_addr):
        cidrs = [x['cidr'] for x in self.get_query_set().values('cidr')]
        return bool(netaddr.all_matching_cidrs(ip_addr, cidrs))


class CIDR(models.Model):
    cidr = models.CharField('CIDR', max_length=128, unique=True,
        help_text='IP addresses and/or subnet')

    objects = Manager()

    def __unicode__(self):
        return self.cidr

