# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0004_auto_20150515_1132'),
    ]

    operations = [
        migrations.AddField(
            model_name='repository',
            name='description',
            field=models.CharField(default='', max_length=500, blank=True),
            preserve_default=False,
        ),
    ]
