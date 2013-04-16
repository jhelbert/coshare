# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Changing field 'Playlist.metric'
        db.alter_column('main_playlist', 'metric', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True))

        # Changing field 'Content.description'
        db.alter_column('main_content', 'description', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True))
    
    
    def backwards(self, orm):
        
        # Changing field 'Playlist.metric'
        db.alter_column('main_playlist', 'metric', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'Content.description'
        db.alter_column('main_content', 'description', self.gf('django.db.models.fields.CharField')(max_length=1000))
    
    
    models = {
        'main.content': {
            'Meta': {'object_name': 'Content'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'main.playlist': {
            'Meta': {'object_name': 'Playlist'},
            'auto_all': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'content': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['main.Content']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metric': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }
    
    complete_apps = ['main']
