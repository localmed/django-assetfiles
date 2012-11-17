"""
Views and functions for serving assets and static files. These are only to be
used during development, and SHOULD NOT be used in a production setting.
"""
import mimetypes
import os
import posixpath
try:
    from urllib.parse import unquote
except ImportError:     # Python 2
    from urllib import unquote

from django.conf import settings
from django.contrib.staticfiles import finders
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404, HttpResponse
from django.views import static

from assetfiles import assets


def serve(request, path, document_root=None, insecure=False, **kwargs):
    """
    Serve static files below a given point in the directory structure or
    from locations inferred from the staticfiles finders.

    To use, put a URL pattern such as::

        (r'^(?P<path>.*)$', 'assetfiles.views.serve')

    in your URLconf.

    It uses the django.views.static view to serve the found files.
    """
    if not settings.DEBUG and not insecure:
        raise ImproperlyConfigured('The staticfiles view can only be used in '
                                   'debug mode or if the the --insecure '
                                   "option of 'runserver' is used")
    normalized_path = posixpath.normpath(unquote(path)).lstrip('/')

    static_path = finders.find(normalized_path)
    if static_path:
        document_root, path = os.path.split(static_path)
        return static.serve(request, path, document_root=document_root, **kwargs)

    asset_path, filter = assets.find(normalized_path)
    if asset_path:
        content = filter.filter(asset_path)
        mimetype, encoding = mimetypes.guess_type(normalized_path)
        return HttpResponse(content, content_type=mimetype)

    if path.endswith('/') or path == '':
        raise Http404('Directory indexes are not allowed here.')
    raise Http404("'%s' could not be found" % path)
