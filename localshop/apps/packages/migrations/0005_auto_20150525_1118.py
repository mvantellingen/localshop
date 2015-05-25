# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('packages', '0004_auto_20150517_1612'),
    ]

    operations = [
        migrations.AddField(
            model_name='repository',
            name='teams',
            field=models.ManyToManyField(related_name='repositories', to='accounts.Team', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='package',
            name='name',
            field=models.SlugField(max_length=200),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='package',
            unique_together=set([('repository', 'name')]),
        ),
    ]
