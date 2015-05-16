# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0006_repository_teams'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repository',
            name='teams',
            field=models.ManyToManyField(related_name='repositories', to='permissions.Team', blank=True),
            preserve_default=True,
        ),
    ]
