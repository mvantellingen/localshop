# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('permissions', '0006_auto_20150516_1923'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='teammember',
            unique_together=set([('team', 'user')]),
        ),
    ]
