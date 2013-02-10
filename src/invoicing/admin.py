from functools import update_wrapper

from django.conf import settings
from django.contrib import admin
from django.contrib.admin.util import unquote
from django.shortcuts import get_object_or_404

import models
from django.template.response import TemplateResponse


class InvoiceLineItemInline(admin.TabularInline):
    model = models.InvoiceLineItem


class PaymentInline(admin.TabularInline):
    model = models.Payment


class InvoiceAdmin(admin.ModelAdmin):
    inlines = [InvoiceLineItemInline, PaymentInline]
    list_display = ('invoice_number', 'customer', 'invoice_date', 'invoice_total', 'paid')
    
    def get_urls(self):
        from django.conf.urls import patterns, url

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.module_name
        
        return patterns('', url(r'^(.+)/print/$', wrap(self.print_view), name='%s_%s_print' % info)) + admin.ModelAdmin.get_urls(self)
    
    def print_view(self, request, object_id, extra_context=None):
        '''Renders a printable view of the invoice.'''
        obj = get_object_or_404(self.model, pk=unquote(object_id))
        context = {
            'object': obj,
            'invoice_address': settings.INVOICE_ADDRESS,
        }
        context.update(extra_context or {})
        return TemplateResponse(request, 'admin/invoicing/print.html', context, current_app=self.admin_site.name)

admin.site.register(models.Invoice, InvoiceAdmin)