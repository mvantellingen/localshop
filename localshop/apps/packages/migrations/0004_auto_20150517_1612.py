# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0003_default_repo'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='repository',
            field=models.ForeignKey(related_name='packages', default=1, to='packages.Repository'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='repository',
            name='description',
            field=models.CharField(default='', max_length=500, blank=True),
            preserve_default=False,
        ),
    ]
