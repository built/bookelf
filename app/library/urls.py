from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from forms import MediaItemSearchForm
from views import *

urlpatterns = patterns('',
    url(r'^$', show_search_form),
    url(r'^search/$', search),
    url(r'^mine/$', show_my_library),
    url(r'^borrowed/$', show_my_borrows),
    url(r'^loaned/$', show_my_loans),
)
