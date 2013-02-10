from django.contrib import admin

import models

class ContactInline(admin.StackedInline):
    '''Allows contacts to be added to customers.'''
    model = models.Contact
    extra = 0

    
class CustomerAdmin(admin.ModelAdmin):
    inlines = (ContactInline, )
    list_display = ('name', 'state', 'phone', 'email')


admin.site.register(models.Customer, CustomerAdmin)