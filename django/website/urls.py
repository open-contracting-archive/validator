from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

from django.contrib import admin
from django.conf import settings
from django.views.generic import RedirectView
admin.autodiscover()

from validator.views import TextFormValidatorView

urlpatterns = patterns('',
    # Examples:
    # url(r'^myapp/', include('myapp.urls')),
    url(r'^$', RedirectView.as_view(pattern_name='home')),
    url(r'^validate/', TextFormValidatorView.as_view(), name='home'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # This requires that static files are served from the 'static' folder.
    # The apache conf is set up to do this for you, but you will need to do it
    # on dev
    (r'^favicon.ico$', RedirectView.as_view(url='{0}images/favicon.ico'.format(settings.STATIC_URL))),
)

if settings.DEBUG:
    urlpatterns = patterns('',
        url(r'^uploads/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        url(r'', include('django.contrib.staticfiles.urls')),
    ) + urlpatterns

#
