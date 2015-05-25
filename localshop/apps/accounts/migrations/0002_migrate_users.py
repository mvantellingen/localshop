# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations



def forwards(apps, schema_editor):

    if 'auth_user' in schema_editor.connection.introspection.table_names():
        migrations.RunSQL(
            "INSERT INTO accounts_user SELECT * FROM auth_user"
        )


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(code=forwards),
    ]
