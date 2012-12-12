import re

from django.conf import settings
from django.conf.urls import patterns, url


def assetfiles_urlpatterns(prefix=None, insecure=False, **kwargs):
    """
    Helper function to return a URL pattern for serving asset files.
    """
    if prefix is None:
        prefix = settings.STATIC_URL
    if (not settings.DEBUG and not insecure) or ('://' in prefix):
        return []

    kwargs['insecure'] = insecure
    return patterns('',
        url(
            r'^%s(?P<path>.*)$' % re.escape(prefix.lstrip('/')),
            'assetfiles.views.serve',
            kwargs=kwargs
        ),
    )
