import datetime
from decimal import Decimal
from functools import update_wrapper

from django.conf import settings
from django.contrib import admin
from django.contrib.admin.options import csrf_protect_m
from django.contrib.admin.util import unquote
from django.db import transaction
from django.shortcuts import get_object_or_404, render
from django.template.response import TemplateResponse

import models
from django.conf.urls import patterns
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

class ContactInline(admin.StackedInline):
    '''Allows contacts to be added to customers.'''
    model = models.Contact
    extra = 0

    
class CustomerAdmin(admin.ModelAdmin):
    inlines = (ContactInline, )
    list_display = ('name', 'state', 'phone', 'email')


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'customer', 'estimate', 'rate')
    @csrf_protect_m
    @transaction.commit_on_success
    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, unquote(object_id))
        
        if extra_context == None:
            extra_context = {}
        
        extra_context['obj'] = obj
        
        return admin.ModelAdmin.change_view(self, request, object_id, form_url=form_url, extra_context=extra_context)

class TimeEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'project', 'start', 'stop', 'description', 'invoice_type', 'invoice_line_item')
    list_editable = ('project', 'start', 'stop', 'description', 'invoice_type')
    
    def get_urls(self):
        from django.conf.urls import patterns, url
        
        urlpatterns = admin.ModelAdmin.get_urls(self)
        
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.module_name
        
        urlpatterns += patterns('',
            url(r'invoice/preview', wrap(self.preview_invoice), name='%s_%s_preview_invoice' % info),
            url(r'invoice/generate', wrap(self.generate_invoice), name='%s_%s_generate_invoice' % info),
        )
        
        return urlpatterns
    
    @csrf_protect_m
    def preview_invoice(self, request, extra_context=None):
        
        data = {
            'entries': models.TimeEntry.get_entries_for_invoicing(),
            'app_label': self.model._meta.app_label, 
            'meta': self.model._meta,
        }
        
        return render(request, 'admin/cm/previewinvoice.html', data)
    
    @csrf_protect_m
    def generate_invoice(self, request, extra_context=None):
        '''Create an invoice from selected TimeEntry records.'''
        HOUR = Decimal(60 * 60)
        entries = request.POST.getlist('timeentry')
        entries = models.TimeEntry.objects.filter(id__in=entries).order_by('project')
        
        line_items = []
        back_refs = []
        if len(entries):
            customer = None
            cur_project = None
            cur_item = None
            cur_list = None
            for entry in entries:
                if customer is None:
                    customer = entry.project.customer
                # prevent an invoice with multiple customers.
                if customer != entry.project.customer:
                    continue
                
                if cur_project is None or cur_project != entry.project:
                    if cur_item is not None:
                        back_refs.append((cur_item, cur_list))
                    cur_list = []
                    cur_project = entry.project
                    cur_item = models.InvoiceLineItem()
                    cur_item.description = cur_project.title
                    cur_item.price = cur_project.rate
                    cur_item.quantity = Decimal(0)
                    line_items.append(cur_item)
                
                cur_item.quantity += Decimal(entry.time_to_invoice().total_seconds()) / HOUR
                cur_list.append(entry)
        
        if cur_item is not None:
            back_refs.append((cur_item, cur_list))
        
        invoice = models.Invoice()
        invoice.customer = customer
        invoice.invoice_number = 'NEW'
        invoice.invoice_date = datetime.date.today()
        invoice.invoice_total = Decimal(0)
        invoice.save()
        
        for item in line_items:
            item.invoice = invoice
            item.save()
        
        for ref in back_refs:
            for entry in ref[1]:
                entry.invoice_line_item = ref[0]
                entry.save()
        
        return HttpResponseRedirect(reverse('admin:cm_invoice_change', args=[invoice.id]))


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


admin.site.register(models.Customer, CustomerAdmin)
admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.TimeEntry, TimeEntryAdmin)
admin.site.register(models.Invoice, InvoiceAdmin)