from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from forms import MediaItemEditor
from views import *

urlpatterns = patterns('',
    url(r'^add/$', show_new_book_form),
    url(r'^save/$', save_book),
    url(r'^isbn/(\d+[Xx]?)/$', view_book), # This captures the isbn which sometimes ends in X.
    url(r'^isbn/([Qq]+[Vv]?\d+)/$', view_book), # Allow a non-ISBN alternate format which always starts with Q's and sometimes starts with Q's plus a V and totals 13 chars.
    url(r'^remove/(\d+)/$', remove_book), # This captures the internal id which is always numeric.
    url(r'^loan/(\d+)/$', loan_book), # This captures the internal book ownership id (aka the ID of the book copy) which is always numeric.
    url(r'^return/(\d+)/$', return_book), # This captures the internal Loan id which is always numeric.
)