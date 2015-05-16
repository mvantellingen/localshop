# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('permissions', '0003_cidr_repository'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cidr',
            name='cidr',
            field=models.CharField(help_text=b'IP addresses and/or subnet', max_length=128, verbose_name=b'CIDR'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='cidr',
            unique_together=set([('repository', 'cidr')]),
        ),
    ]
