# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Project.created'
        db.add_column('cm_project', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2013, 8, 30, 0, 0), blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Project.created'
        db.delete_column('cm_project', 'created')


    models = {
        'cm.contact': {
            'Meta': {'object_name': 'Contact'},
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cm.Customer']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'cm.customer': {
            'Meta': {'object_name': 'Customer'},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'state': ('django.contrib.localflavor.us.models.USStateField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'})
        },
        'cm.invoice': {
            'Meta': {'ordering': "('-invoice_date',)", 'object_name': 'Invoice'},
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cm.Customer']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_date': ('django.db.models.fields.DateField', [], {}),
            'invoice_number': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'invoice_total': ('django.db.models.fields.DecimalField', [], {'max_digits': '18', 'decimal_places': '2'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cm.Project']", 'null': 'True', 'blank': 'True'})
        },
        'cm.invoicelineitem': {
            'Meta': {'ordering': "('invoice', 'id')", 'object_name': 'InvoiceLineItem'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cm.Invoice']"}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '18', 'decimal_places': '2'}),
            'quantity': ('django.db.models.fields.DecimalField', [], {'max_digits': '18', 'decimal_places': '2'})
        },
        'cm.payment': {
            'Meta': {'ordering': "('pay_date',)", 'object_name': 'Payment'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '18', 'decimal_places': '2'}),
            'date_received': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cm.Invoice']"}),
            'pay_date': ('django.db.models.fields.DateField', [], {}),
            'payment_type': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'transaction_number': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'cm.project': {
            'Meta': {'object_name': 'Project'},
            'complete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cm.Customer']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'estimate': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rate': ('django.db.models.fields.DecimalField', [], {'default': "'45.0'", 'max_digits': '20', 'decimal_places': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cm.timeentry': {
            'Meta': {'ordering': "('-start',)", 'object_name': 'TimeEntry'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_line_item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cm.InvoiceLineItem']", 'null': 'True', 'blank': 'True'}),
            'invoice_type': ('django.db.models.fields.CharField', [], {'default': "'invoice'", 'max_length': '50'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cm.Project']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'stop': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['cm']