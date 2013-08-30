from decimal import Decimal
import datetime

from django.db import models
from django.contrib.localflavor.us.models import USStateField
from django.conf.urls.static import static

PAYMENT_TYPES = (
    ('cash', 'Cash'),
    ('check', 'Check'),
    ('credit card', 'Credit Card'),
)


# Create your models here.
class Customer(models.Model):
    '''A customer that service is provided for.'''
    name = models.CharField(max_length=500)
    address1 = models.CharField(max_length=1000, blank=True)
    address2 = models.CharField(max_length=1000, blank=True)
    city = models.CharField(max_length=255, blank=True)
    state = USStateField(blank=True, null=True)
    postal_code = models.CharField(max_length=30, blank=True)
    phone = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    notes = models.TextField(blank=True)
    
    def __unicode__(self):
        '''Returns a human readable version of the object.'''
        return self.name


class Contact(models.Model):
    '''A contact for a customer.'''
    customer = models.ForeignKey(Customer)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    
    def __unicode__(self):
        '''Returns a human readable version of the object.'''
        return u'%s %s' % (self.first_name, self.last_name)


class Project(models.Model):
    '''A project for a customer.'''
    customer = models.ForeignKey(Customer)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    estimate = models.DecimalField(max_digits=20, decimal_places=4)
    rate = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('45.0'))
    created = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    
    def __unicode__(self):
        '''Renders a human readable string of the object.'''
        return u'%s - %s' % (self.customer, self.title)
    
    def time_spent(self):
        '''Calculates the total time spent on the project.'''
        total = datetime.timedelta()
        for timeentry in self.timeentry_set.all():
            total += timeentry.time_spent()
        return total


class TimeEntry(models.Model):
    '''Tracks time spent on a project.'''
    INVOICE_TYPE_CHOICES = (
        ('invoice', 'Invoice'),
        ('eatit', 'Eat It'),
    )
    
    class Meta:
        verbose_name = 'Time Entry'
        verbose_name_plural = 'Time Entries'
        ordering = ('-start', )
    
    project = models.ForeignKey(Project)
    description = models.TextField(blank=True)
    start = models.DateTimeField()
    stop = models.DateTimeField(blank=True, null=True)
    invoice_type = models.CharField(max_length=50, choices=INVOICE_TYPE_CHOICES, default='invoice')
    invoice_line_item = models.ForeignKey('InvoiceLineItem', null=True, blank=True)
    
    def __unicode__(self):
        '''Renders a human readable string of the object.'''
        return u'%s - %s : %s' % (self.start, self.stop, self.description)
    
    def time_spent(self):
        '''Calculates the TimeDelta of the stop and start times.'''
        if not self.stop:
            return datetime.timedelta(0)
        
        return self.stop - self.start
    
    def time_to_invoice(self):
        '''Calculates the TimeDelta of the stop and start times to 5 min increments.'''
        # TODO: if total invoiced time is greater than estimate then return timedelta(0)
        delta = self.time_spent()
        seconds = delta.total_seconds()
        five_minutes = 60 * 5
        if seconds % five_minutes > 0:
            return datetime.timedelta(seconds=(int(seconds / five_minutes) + 1) * five_minutes)
        else:
            return delta
        
    
    @staticmethod
    def get_entries_for_invoicing():
        return TimeEntry.objects.filter(invoice_line_item=None, invoice_type='invoice', project__complete=False, stop__isnull=False)


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

