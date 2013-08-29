# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Customer'
        db.create_table('cm_customer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('address1', self.gf('django.db.models.fields.CharField')(max_length=1000, blank=True)),
            ('address2', self.gf('django.db.models.fields.CharField')(max_length=1000, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('state', self.gf('django.contrib.localflavor.us.models.USStateField')(max_length=2, null=True, blank=True)),
            ('postal_code', self.gf('django.db.models.fields.CharField')(max_length=30, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('cm', ['Customer'])

        # Adding model 'Contact'
        db.create_table('cm_contact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cm.Customer'])),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('cm', ['Contact'])

        # Adding model 'Project'
        db.create_table('cm_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cm.Customer'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('estimate', self.gf('django.db.models.fields.DecimalField')(max_digits=20, decimal_places=4)),
            ('rate', self.gf('django.db.models.fields.DecimalField')(default='45.0', max_digits=20, decimal_places=2)),
            ('complete', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('cm', ['Project'])

        # Adding model 'TimeEntry'
        db.create_table('cm_timeentry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cm.Project'])),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('stop', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('invoice_line_item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cm.InvoiceLineItem'], null=True, blank=True)),
        ))
        db.send_create_signal('cm', ['TimeEntry'])

        # Adding model 'Invoice'
        db.create_table('cm_invoice', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('invoice_number', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('customer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cm.Customer'])),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cm.Project'], null=True, blank=True)),
            ('invoice_date', self.gf('django.db.models.fields.DateField')()),
            ('invoice_total', self.gf('django.db.models.fields.DecimalField')(max_digits=18, decimal_places=2)),
            ('paid', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('cm', ['Invoice'])

        # Adding model 'InvoiceLineItem'
        db.create_table('cm_invoicelineitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('invoice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cm.Invoice'])),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('quantity', self.gf('django.db.models.fields.DecimalField')(max_digits=18, decimal_places=2)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=18, decimal_places=2)),
        ))
        db.send_create_signal('cm', ['InvoiceLineItem'])

        # Adding model 'Payment'
        db.create_table('cm_payment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('invoice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cm.Invoice'])),
            ('payment_type', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('transaction_number', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('date_received', self.gf('django.db.models.fields.DateField')()),
            ('pay_date', self.gf('django.db.models.fields.DateField')()),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=18, decimal_places=2)),
        ))
        db.send_create_signal('cm', ['Payment'])


    def backwards(self, orm):
        # Deleting model 'Customer'
        db.delete_table('cm_customer')

        # Deleting model 'Contact'
        db.delete_table('cm_contact')

        # Deleting model 'Project'
        db.delete_table('cm_project')

        # Deleting model 'TimeEntry'
        db.delete_table('cm_timeentry')

        # Deleting model 'Invoice'
        db.delete_table('cm_invoice')

        # Deleting model 'InvoiceLineItem'
        db.delete_table('cm_invoicelineitem')

        # Deleting model 'Payment'
        db.delete_table('cm_payment')


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
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cm.Customer']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'estimate': ('django.db.models.fields.DecimalField', [], {'max_digits': '20', 'decimal_places': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rate': ('django.db.models.fields.DecimalField', [], {'default': "'45.0'", 'max_digits': '20', 'decimal_places': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'cm.timeentry': {
            'Meta': {'object_name': 'TimeEntry'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_line_item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cm.InvoiceLineItem']", 'null': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cm.Project']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'stop': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['cm']