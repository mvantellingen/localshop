# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0004_auto_20150515_1132'),
        ('permissions', '0002_auto_20150515_1943'),
    ]

    operations = [
        migrations.AddField(
            model_name='cidr',
            name='repository',
            field=models.ForeignKey(related_name='cidr_list', default=1, to='packages.Repository'),
            preserve_default=False,
        ),
    ]
