# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations


def forwards(apps, schema_editor):
    Repository = apps.get_model('packages', 'Repository')
    Repository.objects.create(name='Default', slug='default')


def backwards(apps, schema_editor):
    Repository = apps.get_model('packages', 'Repository')
    Repository.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0002_repository'),
    ]

    operations = [
        migrations.RunPython(
            code=forwards,
            reverse_code=backwards),
    ]
