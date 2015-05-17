# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('packages', '0004_auto_20150517_1612'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('permissions', '0002_remove_userena'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=500, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TeamMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('role', models.CharField(max_length=100, choices=[(b'owner', 'Owner'), (b'developer', 'Developer')])),
                ('team', models.ForeignKey(related_name='members', to='permissions.Team')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='teammember',
            unique_together=set([('team', 'user')]),
        ),
        migrations.AddField(
            model_name='team',
            name='users',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, through='permissions.TeamMember'),
            preserve_default=True,
        ),
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
            preserve_default=True,
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
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='credential',
            name='created',
            field=model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='cidr',
            unique_together=set([('repository', 'cidr')]),
        ),
    ]
