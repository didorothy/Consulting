from decimal import Decimal

from django.db import models

from customer.models import Customer
from timetracking.models import Project

PAYMENT_TYPES = (
    ('cash', 'Cash'),
    ('check', 'Check'),
    ('credit card', 'Credit Card'),
)

# Create your models here.
class Invoice(models.Model):
    class Meta:
        ordering = ('-invoice_date', )
    
    invoice_number = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer)
    project = models.ForeignKey(Project, null=True, blank=True)
    invoice_date = models.DateField()
    invoice_total = models.DecimalField(max_digits=18, decimal_places=2)
    paid = models.BooleanField()
    
    def __unicode__(self):
        '''Returns a human readable version of the instance.'''
        return u'%s - %s' % (self.invoice_number, self.customer)
    
    def total(self):
        '''Returns the total charge for the invoice.'''
        total = Decimal('0')
        for item in self.invoicelineitem_set.all():
            total += item.total()
        return total


class InvoiceLineItem(models.Model):
    class Meta:
        ordering = ('invoice', 'id')
    
    invoice = models.ForeignKey(Invoice)
    description = models.CharField(max_length=500)
    quantity = models.DecimalField(max_digits=18, decimal_places=2)
    price = models.DecimalField(max_digits=18, decimal_places=2)
    
    def __unicode__(self):
        '''Returns a human readable version of the instance.'''
        return u'%s - %s %s %s' % (self.invoice.invoice_number, self.description, self.quantity, self.price)
    
    def total(self):
        '''Returns the total cost for the item.'''
        return self.quantity * self.price


class Payment(models.Model):
    class Meta:
        ordering = ('pay_date', )
    
    invoice = models.ForeignKey(Invoice)
    payment_type = models.CharField(max_length=30, choices=PAYMENT_TYPES)
    transaction_number = models.CharField(max_length=50)
    date_received = models.DateField()
    pay_date = models.DateField() # when the payment was written.
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    
    def __unicode__(self):
        '''Returns a human readable version of the instance.'''
        return u'%s - %s %s' % (self.invoice.invoice_number, self.pay_date, self.amount)

