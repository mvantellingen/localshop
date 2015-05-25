# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations



class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20150525_1040'),
    ]

    operations = [
        migrations.RunSQL(
            "INSERT INTO accounts_user SELECT * FROM auth_user"
        )
    ]
