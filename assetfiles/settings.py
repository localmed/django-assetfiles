from django.conf import settings


FILTERS = getattr(settings, 'ASSETFILES_FILTERS', (
    'assetfiles.filters.sass.SassFilter',
    'assetfiles.filters.coffee.CoffeeScriptFilter'
))

SASS_DIRS = getattr(settings, 'ASSETFILES_SASS_DIRS', ('css',))

SASS_OPTIONS = getattr(settings, 'ASSETFILES_SASS_OPTIONS', {})

COFFEE_SCRIPT_OPTIONS = getattr(settings,
                                'ASSETFILES_COFFEE_SCRIPT_OPTIONS', {})
