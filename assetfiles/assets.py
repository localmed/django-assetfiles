from django.contrib.staticfiles import finders

from assetfiles import filters

def find(output_path):
    """
    Search for filters by the given output path. If one is found, search for
    one the filter's possible input paths for the given output path. If there's
    a match return a tuple of the found absolute path and the found filter.
    Otherwise return tuple of (None, None).
    """
    filter = filters.find_by_output_path(output_path)
    if filter:
        for possible_path in filter.possible_input_paths(output_path):
            full_path = finders.find(possible_path)
            if full_path: return full_path, filter
    return None, None
