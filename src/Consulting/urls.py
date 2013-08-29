from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

import jsonrpc
#import timetracking.api # required to get the json-rpc api to work properly.

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Consulting.views.home', name='home'),
    # url(r'^Consulting/', include('Consulting.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    #url(r'^json-rpc/browse/$', 'jsonrpc.views.browse', name='jsonrpc_browser'),
    #url(r'^json-rpc/', jsonrpc.jsonrpc_site.dispatch, name='jsonrpc_mountpoint'),
    
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
