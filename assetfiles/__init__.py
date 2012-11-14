from django.contrib.staticfiles import finders
from django.core.exceptions import ImproperlyConfigured
from django.utils.datastructures import SortedDict
from django.utils.functional import memoize
from django.utils.importlib import import_module

from assetfiles import settings
from assetfiles.filters.base import BaseFilter

def filter_from_path(intput_path):
    """
    Return the first filter instance that would accept the given path as input.
    """
    for filter in get_filters():
        if filter.matches_input(intput_path):
            return filter
    return None

def filter_to_path(output_path):
    """
    Return the first filter instance that would output the given path.
    """
    for filter in get_filters():
        if filter.matches_output(output_path):
            return filter
    return None

def find_asset(output_path):
    """
    Search for filters by the given output path. If one is found, search for
    one the filter's possible input paths for the given output path. If there's
    a match return a tuple of the found absolute path and the found filter.
    Otherwise return tuple of (None, None).
    """
    filter = filter_to_path(output_path)
    if filter:
        for possible_path in filter.possible_input_paths(output_path):
            full_path = finders.find(possible_path)
            if full_path: return full_path, filter
    return None, None

def get_filters():
    """
    Return filter instances configured in settings.ASSETFILES_FILTERS.
    """
    for filter_path in settings.FILTERS:
        yield get_filter(filter_path)

def _get_filter(import_path):
    """
    Imports the assetfiles filter class described by import_path, where
    import_path is the full Python path to the class.
    """
    module, attr = import_path.rsplit('.', 1)
    try:
        mod = import_module(module)
    except ImportError as e:
        raise ImproperlyConfigured('Error importing module %s: "%s"' %
                                   (module, e))
    try:
        Filter = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured('Module "%s" does not define a "%s" '
                                   'class.' % (module, attr))
    if not issubclass(Filter, BaseFilter):
        raise ImproperlyConfigured('Filter "%s" is not a subclass of "%s"' %
                                   (Filter, BaseFilter))
    return Filter()

_filters = SortedDict()
get_filter = memoize(_get_filter, _filters, 1)
