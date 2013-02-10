from decimal import Decimal
import datetime

from django.db import models

from customer.models import Customer

# Create your models here.
class Project(models.Model):
    '''A project for a customer.'''
    customer = models.ForeignKey(Customer)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    estimate = models.DecimalField(max_digits=20, decimal_places=4)
    rate = models.DecimalField(max_digits=20, decimal_places=2, default=Decimal('45.0'))
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
    project = models.ForeignKey(Project)
    description = models.TextField(blank=True)
    start = models.DateTimeField()
    stop = models.DateTimeField(blank=True, null=True)
    invoice_line_item = models.ForeignKey('invoicing.InvoiceLineItem', null=True, blank=True)
    
    def __unicode__(self):
        '''Renders a human readable string of the object.'''
        return u'%s - %s : %s' % (self.start, self.stop, self.description)
    
    def time_spent(self):
        '''Calculates the TimeDelta of the stop and start times.'''
        if not self.stop:
            return Decimal('0')
        
        return self.stop - self.start

