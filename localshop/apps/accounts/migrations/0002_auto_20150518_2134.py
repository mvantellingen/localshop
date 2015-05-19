# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import uuidfield.fields
import model_utils.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessKey',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False)),
                ('access_key', uuidfield.fields.UUIDField(blank=True, max_length=32, editable=False, verbose_name='Access key', unique=True, help_text='The access key', db_index=True)),
                ('secret_key', uuidfield.fields.UUIDField(blank=True, max_length=32, editable=False, verbose_name='Secret key', unique=True, help_text='The secret key', db_index=True)),
                ('comment', models.CharField(default='', blank=True, max_length=255, help_text="A comment about this credential, e.g. where it's being used", null=True)),
                ('last_usage', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(related_name='access_keys', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='teammember',
            name='role',
            field=models.CharField(choices=[('owner', 'Owner'), ('developer', 'Developer')], max_length=100),
            preserve_default=True,
        ),
    ]
