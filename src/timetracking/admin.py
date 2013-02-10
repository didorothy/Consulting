from functools import update_wrapper

from django.contrib import admin
from django.contrib.admin.options import csrf_protect_m
from django.contrib.admin.util import unquote
from django.db import transaction

import models

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
    pass
#    def get_urls(self):
#        from django.conf.urls import patterns, url

#        def wrap(view):
#            def wrapper(*args, **kwargs):
#                return self.admin_site.admin_view(view)(*args, **kwargs)
#            return update_wrapper(wrapper, view)

#        info = self.model._meta.app_label, self.model._meta.module_name

#        urlpatterns = patterns('',
#            url(r'^$',
#                wrap(self.changelist_view),
#                name='%s_%s_changelist' % info),
#            url(r'^add/$',
#                wrap(self.add_view),
#                name='%s_%s_add' % info),
#            url(r'^(.+)/history/$',
#                wrap(self.history_view),
#                name='%s_%s_history' % info),
#            url(r'^(.+)/delete/$',
#                wrap(self.delete_view),
#                name='%s_%s_delete' % info),
#            url(r'^(.+)/$',
#                wrap(self.change_view),
#                name='%s_%s_change' % info),
#        )
#        return urlpatterns


admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.TimeEntry, TimeEntryAdmin)