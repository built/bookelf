from django.conf.urls.defaults import *
from django.conf import settings

from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()

from django.contrib.auth.decorators import login_required

from library.views import show_leaderboard

@login_required
def guardian(request):
	return include('basic_profiles.urls')


import os

urlpatterns = patterns('',
    url(r'^$', direct_to_template, {"template": "homepage.html"}, name="home"),
    
    (r'^about/', include('about.urls')),
    (r'^account/', include('account.urls')),
    (r'^openid/', include('account.openid_urls')),
    (r'^profiles/', include('basic_profiles.urls')),
# TO DO: Make profiles protected from non-logged-in people. 
# (Right now it breaks the reverse url look up if we try.)
#    (r'^profiles/', guardian), 
    (r'^notices/', include('notification.urls')),
    (r'^announcements/', include('announcements.urls')),
    (r'^library/', include('library.urls')),
    (r'^book/', include('book.urls')),

    (r'^leaderboard/', show_leaderboard),
    
    (r'^admin/(.*)', admin.site.root),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': os.path.join(os.path.dirname(__file__), "site_media")}),
    )
