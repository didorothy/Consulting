from django.db import models
from django.contrib.localflavor.us.models import USStateField

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
