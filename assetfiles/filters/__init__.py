from django.core.exceptions import ImproperlyConfigured
from django.utils.datastructures import SortedDict
from django.utils.functional import memoize
from django.utils.importlib import import_module

from assetfiles import settings
from assetfiles.filters.base import BaseFilter


def find_by_input_path(intput_path):
    """
    Returns the first filter that would accept the given path as input.

    Args:
        input_path: An absolute path to the file
    Returns:
        The found filter instance or `None`
    """
    for filter in get_filters():
        if filter.matches_input(intput_path):
            return filter
    return None


def find_by_output_path(output_path):
    """
    Returns the first filter that would output to the given path.

    Args:
        output_path: An absolute path to the file
    Returns:
        The found filter instance or `None`
    """
    for filter in get_filters():
        if filter.matches_output(output_path):
            return filter
    return None


def get_filters():
    """
    Returns filter instances configured in ASSETFILES_FILTERS.
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
