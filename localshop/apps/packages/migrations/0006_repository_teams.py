# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('permissions', '0003_cidr_repository'),
        ('packages', '0005_repository_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='repository',
            name='teams',
            field=models.ManyToManyField(related_name='repositories', to='permissions.Team'),
            preserve_default=True,
        ),
    ]
