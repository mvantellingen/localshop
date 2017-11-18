# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0006_repository_upstream_pypi_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='releasefile',
            name='python_version',
            field=models.CharField(max_length=50),
            preserve_default=True,
        ),
    ]
