from djangbone.views import BackboneAPIView

import models

# TODO: build forms to allow for editing.

class CustomerView(BackboneAPIView):
    base_queryset = models.Customer.objects.all()
    serialize_fields = ('id', 'name', 'address1', 'address2', 'city', 'state', 'postal_code', 'phone', 'email', 'notes')


class ContactView(BackboneAPIView):
    base_queryset = models.Contact.objects.all()
    serialize_fields = ('id', 'customer', 'first_name', 'last_name', 'email', 'phone', 'notes')


class ProjectView(BackboneAPIView):
    base_queryset = models.Project.objects.all()
    serialize_fields = ('id', 'customer', 'title', 'description', 'estimate', 'rate', 'complete')


class TimeEntryView(BackboneAPIView):
    base_queryset = models.TimeEntry.objects.all()
    serialize_fields = ('id', 'project', 'description', 'start', 'stop', 'invoice_line_item')


class InvoiceView(BackboneAPIView):
    base_queryset = models.Invoice.objects.all()
    serialize_fields = ('id', 'invoice_number', 'customer', 'project', 'invoice_date', 'invoice_total', 'paid')


class InvoiceLineItemView(BackboneAPIView):
    base_queryset = models.InvoiceLineItem.objects.all()
    serialize_fields = ('id', 'invoice', 'description', 'quantity', 'price')


class PaymentView(BackboneAPIView):
    base_queryset = models.Payment.objects.all()
    serialize_fields = ('id', 'invoice', 'payment_type', 'transaction_number', 'date_received', 'pay_date', 'amount')

