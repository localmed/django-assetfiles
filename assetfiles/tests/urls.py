import re

from django.conf import settings
from django.conf.urls import patterns, url


# URL conf for static files taken from django.conf.urls.static.
# Customized to include insecure=True, because tests are run with DEBUG=False.
urlpatterns = patterns('',
    url(r'^%s(?P<path>.*)$' % re.escape(settings.STATIC_URL.lstrip('/')),
        'assetfiles.views.serve', {'insecure': True}),
)
