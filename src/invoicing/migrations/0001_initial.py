# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Invoice'
        db.create_table('invoicing_invoice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('invoice_number', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['customer.Customer'])),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['timetracking.Project'], null=True, blank=True)),
            ('invoice_date', self.gf('django.db.models.fields.DateField')()),
            ('invoice_total', self.gf('django.db.models.fields.DecimalField')(max_digits=18, decimal_places=2)),
            ('paid', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('invoicing', ['Invoice'])

        # Adding model 'InvoiceLineItem'
        db.create_table('invoicing_invoicelineitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('invoice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['invoicing.Invoice'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('quantity', self.gf('django.db.models.fields.DecimalField')(max_digits=18, decimal_places=2)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=18, decimal_places=2)),
            ('time_entry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['timetracking.TimeEntry'], null=True, blank=True)),
        ))
        db.send_create_signal('invoicing', ['InvoiceLineItem'])

        # Adding model 'Payment'
        db.create_table('invoicing_payment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('invoice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['invoicing.Invoice'])),
            ('payment_type', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('transaction_number', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('date_received', self.gf('django.db.models.fields.DateField')()),
            ('pay_date', self.gf('django.db.models.fields.DateField')()),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=18, decimal_places=2)),
        ))
        db.send_create_signal('invoicing', ['Payment'])


    def backwards(self, orm):
        # Deleting model 'Invoice'
        db.delete_table('invoicing_invoice')

        # Deleting model 'InvoiceLineItem'
        db.delete_table('invoicing_invoicelineitem')

        # Deleting model 'Payment'
        db.delete_table('invoicing_payment')


    models = {
        'customer.customer': {
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
        'invoicing.invoice': {
            'Meta': {'ordering': "('-invoice_date',)", 'object_name': 'Invoice'},
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['customer.Customer']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_date': ('django.db.models.fields.DateField', [], {}),
            'invoice_number': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'invoice_total': ('django.db.models.fields.DecimalField', [], {'max_digits': '18', 'decimal_places': '2'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['timetracking.Project']", 'null': 'True', 'blank': 'True'})
        },
        'invoicing.invoicelineitem': {
            'Meta': {'ordering': "('invoice', 'id')", 'object_name': 'InvoiceLineItem'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['invoicing.Invoice']"}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '18', 'decimal_places': '2'}),
            'quantity': ('django.db.models.fields.DecimalField', [], {'max_digits': '18', 'decimal_places': '2'}),
            'time_entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['timetracking.TimeEntry']", 'null': 'True', 'blank': 'True'})
        },
        'invoicing.payment': {
            'Meta': {'ordering': "('pay_date',)", 'object_name': 'Payment'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '18', 'decimal_places': '2'}),
            'date_received': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['invoicing.Invoice']"}),
            'pay_date': ('django.db.models.fields.DateField', [], {}),
            'payment_type': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'transaction_number': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'timetracking.project': {
            'Meta': {'object_name': 'Project'},
            'complete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['customer.Customer']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'estimate': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rate': ('django.db.models.fields.DecimalField', [], {'default': "'45.0'", 'max_digits': '20', 'decimal_places': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'timetracking.timeentry': {
            'Meta': {'object_name': 'TimeEntry'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['timetracking.Project']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'stop': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['invoicing']