from django.conf.urls import patterns, include, url
from django.http import HttpResponse

def index(request):
    return HttpResponse("Welcome to Book Elf")


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', index, name='home'),
    # url(r'^bookelf/', include('bookelf.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
