# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'CIDR.label'
        db.add_column('permissions_cidr', 'label',
                      self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True),
                      keep_default=False)

        # Adding unique constraint on 'CIDR', fields ['cidr']
        db.create_unique('permissions_cidr', ['cidr'])


    def backwards(self, orm):
        # Removing unique constraint on 'CIDR', fields ['cidr']
        db.delete_unique('permissions_cidr', ['cidr'])

        # Deleting field 'CIDR.label'
        db.delete_column('permissions_cidr', 'label')


    models = {
        'permissions.cidr': {
            'Meta': {'object_name': 'CIDR'},
            'cidr': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['permissions']