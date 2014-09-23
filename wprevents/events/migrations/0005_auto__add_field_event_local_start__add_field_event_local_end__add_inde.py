# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Event.local_start'
        db.add_column(u'events_event', 'local_start',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now),
                      keep_default=False)

        # Adding field 'Event.local_end'
        db.add_column(u'events_event', 'local_end',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now),
                      keep_default=False)

        # Adding index on 'Instance', fields ['event', 'start']
        db.create_index(u'events_instance', ['event_id', 'start'])


    def backwards(self, orm):
        # Removing index on 'Instance', fields ['event', 'start']
        db.delete_index(u'events_instance', ['event_id', 'start'])

        # Deleting field 'Event.local_start'
        db.delete_column(u'events_event', 'local_start')

        # Deleting field 'Event.local_end'
        db.delete_column(u'events_event', 'local_end')


    models = {
        u'events.event': {
            'Meta': {'object_name': 'Event', 'index_together': "[['title', 'start', 'end']]"},
            'areas': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['events.FunctionalArea']", 'symmetrical': 'False', 'blank': 'True'}),
            'bulk_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'details': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_end': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'local_start': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'recurrence': ('recurrence.fields.RecurrenceModelField', [], {'to': u"orm['recurrence.Recurrence']", 'unique': 'True', 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '120', 'blank': 'True'}),
            'space': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'events_hosted'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['events.Space']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        },
        u'events.functionalarea': {
            'Meta': {'object_name': 'FunctionalArea'},
            'color': ('django.db.models.fields.CharField', [], {'default': "'red-1'", 'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'events.instance': {
            'Meta': {'object_name': 'Instance', 'index_together': "[['event', 'start']]"},
            'end': ('django.db.models.fields.DateTimeField', [], {}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'instances'", 'to': u"orm['events.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'events.space': {
            'Meta': {'object_name': 'Space'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'country': ('django.db.models.fields.CharField', [], {'default': "'US'", 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'lon': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'photo': ('django.db.models.fields.files.FileField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'timezone': ('django.db.models.fields.CharField', [], {'default': "'UTC'", 'max_length': '100'})
        },
        u'recurrence.recurrence': {
            'Meta': {'object_name': 'Recurrence'},
            'dtend': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'dtstart': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['events']