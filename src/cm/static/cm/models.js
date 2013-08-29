(function($) {
	
	window.CM = window.CM || {};
	var M = window.CM.Models = window.CM.Models || {};
	
	M.Customer = Backbone.Model.extend({
		defaults: {
			name: '',
			address1: '',
			address2: '',
			city: '', 
			state: '',
			postal_code: '',
			phone: '',
			email: '',
			notes: ''
		}
	});
	
	M.CustomerCollection = Backbone.Collection.extend({
		model: M.Customer
	});
	
	M.Contact = Backbone.Model.extend({
		defaults: {
			customer: -1,
			first_name: '',
			last_name: '',
			email: '',
			phone: '',
			notes: ''
		}
	});
	
	M.ContactCollection = Backbone.Collection.extend({
		model: M.Contact
	});
	
	M.Project = Backbone.Model.extend({
		defaults: {
			customer: -1,
			title: '',
			description: '',
			estimate: 0,
			rate: 45,
			complete: false
		}
	});
	
	M.ProjectCollection = Backbone.Collection.extend({
		model: M.Project
	});
	
	M.TimeEntry = Backbone.Model.extend({
		defaults: {
			project: -1,
			description: '',
			start: new Date(),
			stop: null,
			invoice_line_item: null
		}
	});
	
	M.TimeEntryCollection = Backbone.Collection.extend({
		model: M.TimeEntry
	});
	
	M.Invoice = Backbone.Model.extend({
		defaults: {
			invoice_number: null,
			customer: -1,
			project: null,
			invoice_date: new Date(),
			invoice_total: 0,
			paid: false
		}
	});
	
	M.InvoiceCollection = Backbone.Collection.extend({
		model: M.Invoice
	});
	
	M.InvoiceLineItem = Backbone.Model.extend({
		defaults: {
			invoice: -1,
			description: '',
			quantity: 0,
			price: 0
		}
	});
	
	M.InvoiceLineItemCollection = Backbone.Collection.extend({
		model: M.InvoiceLineItem
	});
	
	M.Payment = Backbone.Model.extend({
		defaults: {
			invoice: -1,
			payment_type: 'check',
			transaction_number: '',
			date_received: new Date(),
			pay_date: new Date(),
			amount: 0
		}
	});
	
	M.PaymentCollection = Backbone.Collection.extend({
		model: M.Payment
	});
	
})(jQuery)
