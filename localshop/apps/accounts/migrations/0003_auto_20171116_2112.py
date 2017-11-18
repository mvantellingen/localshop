# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-16 21:12
from __future__ import unicode_literals

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_migrate_users'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='accesskey',
            name='access_key',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, help_text='The access key', verbose_name='Access key'),
        ),
        migrations.AlterField(
            model_name='accesskey',
            name='comment',
            field=models.CharField(blank=True, default='', help_text="A comment about this credential, e.g. where it's being used", max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='accesskey',
            name='secret_key',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, help_text='The secret key', verbose_name='Secret key'),
        ),
        migrations.AlterField(
            model_name='teammember',
            name='role',
            field=models.CharField(choices=[('owner', 'Owner'), ('developer', 'Developer')], max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username'),
        ),
    ]
