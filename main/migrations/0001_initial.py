# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Content'
        db.create_table('main_content', (
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1000)),
        ))
        db.send_create_signal('main', ['Content'])

        # Adding model 'Playlist'
        db.create_table('main_playlist', (
            ('auto_all', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('metric', self.gf('django.db.models.fields.IntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('main', ['Playlist'])

        # Adding M2M table for field content on 'Playlist'
        db.create_table('main_playlist_content', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('playlist', models.ForeignKey(orm['main.playlist'], null=False)),
            ('content', models.ForeignKey(orm['main.content'], null=False))
        ))
        db.create_unique('main_playlist_content', ['playlist_id', 'content_id'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Content'
        db.delete_table('main_content')

        # Deleting model 'Playlist'
        db.delete_table('main_playlist')

        # Removing M2M table for field content on 'Playlist'
        db.delete_table('main_playlist_content')
    
    
    models = {
        'main.content': {
            'Meta': {'object_name': 'Content'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'main.playlist': {
            'Meta': {'object_name': 'Playlist'},
            'auto_all': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'content': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['main.Content']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metric': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }
    
    complete_apps = ['main']
