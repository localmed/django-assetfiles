from django.conf import settings


FILTERS = getattr(settings, 'ASSETFILES_FILTERS', (
    'assetfiles.filters.sass.SassFilter',
))

SASS_DIRS = getattr(settings, 'ASSETFILES_SASS_DIRS', ('css',))
