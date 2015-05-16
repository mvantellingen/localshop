# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('permissions', '0005_auto_20150516_1858'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='credential',
            name='creator',
        ),
        migrations.AlterField(
            model_name='credential',
            name='allow_upload',
            field=models.BooleanField(default=True, help_text='Indicate if these credentials allow uploading new files'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='credential',
            name='created',
            field=model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='credential',
            name='repository',
            field=models.ForeignKey(related_name='credentials', to='packages.Repository'),
            preserve_default=True,
        ),
    ]
