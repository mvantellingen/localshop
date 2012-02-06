# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'CIDR'
        db.create_table('permissions_cidr', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cidr', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('permissions', ['CIDR'])


    def backwards(self, orm):
        
        # Deleting model 'CIDR'
        db.delete_table('permissions_cidr')


    models = {
        'permissions.cidr': {
            'Meta': {'object_name': 'CIDR'},
            'cidr': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['permissions']
