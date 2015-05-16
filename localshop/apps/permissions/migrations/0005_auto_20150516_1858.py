# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0007_auto_20150516_1825'),
        ('permissions', '0004_auto_20150516_1825'),
    ]

    operations = [
        migrations.AddField(
            model_name='credential',
            name='allow_upload',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='credential',
            name='repository',
            field=models.ForeignKey(default=1, to='packages.Repository'),
            preserve_default=False,
        ),
    ]
