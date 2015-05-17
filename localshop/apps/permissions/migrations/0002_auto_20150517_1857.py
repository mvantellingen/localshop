# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0005_auto_20150517_1857'),
        ('permissions', '0001_squashed_0002_remove_userena'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='credential',
            name='creator',
        ),
        migrations.AddField(
            model_name='cidr',
            name='repository',
            field=models.ForeignKey(related_name='cidr_list', default=1, to='packages.Repository'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='credential',
            name='allow_upload',
            field=models.BooleanField(default=True, help_text='Indicate if these credentials allow uploading new files'),
        ),
        migrations.AddField(
            model_name='credential',
            name='repository',
            field=models.ForeignKey(related_name='credentials', default=1, to='packages.Repository'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cidr',
            name='cidr',
            field=models.CharField(help_text=b'IP addresses and/or subnet', max_length=128, verbose_name=b'CIDR'),
        ),
        migrations.AlterField(
            model_name='credential',
            name='created',
            field=model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AlterUniqueTogether(
            name='cidr',
            unique_together=set([('repository', 'cidr')]),
        ),
    ]
