"""
Views and functions for serving static files. These are only to be used during
development, and SHOULD NOT be used in a production setting.
"""
import os, posixpath
try:
    from urllib.parse import unquote
except ImportError:     # Python 2
    from urllib import unquote

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404, HttpResponse
from django.views import static

from django.contrib.staticfiles import finders

def serve(request, path, document_root=None, insecure=False, **kwargs):
    """
    Serve static files below a given point in the directory structure or
    from locations inferred from the staticfiles finders.

    To use, put a URL pattern such as::

        (r'^(?P<path>.*)$', 'django.contrib.staticfiles.views.serve')

    in your URLconf.

    It uses the django.views.static view to serve the found files.
    """
    if not settings.DEBUG and not insecure:
        raise ImproperlyConfigured('The staticfiles view can only be used in '
                                   'debug mode or if the the --insecure '
                                   "option of 'runserver' is used")
    normalized_path = posixpath.normpath(unquote(path)).lstrip('/')
    absolute_path = finders.find(normalized_path)

    if absolute_path:
        document_root, path = os.path.split(absolute_path)
        return static.serve(request, path, document_root=document_root, **kwargs)

    if normalized_path.endswith('.css'):
        scss_path = normalized_path.replace('.css', '.scss')
        absolute_scss_path = finders.find(scss_path)
        if absolute_scss_path:
            from assetfiles.processors import SassProcessor
            css = SassProcessor(absolute_scss_path).process()
            return HttpResponse(css, content_type='text/css')

    if path.endswith('/') or path == '':
        raise Http404('Directory indexes are not allowed here.')
    raise Http404("'%s' could not be found" % path)
