from django.contrib.staticfiles import finders

from assetfiles import filters


def find(output_path):
    """
    Search for filters that would output the given file.

    If one is found, search for one the filter's possible input paths for
    the given output path. If there's a match return a tuple of the found
    absolute path and the found filter. Otherwise return tuple of (None, None).

    Args:
        output_path: An absolute path to search for.
    Returns
        A tuple containing the absolute path to the input file and the filter
        instance that would filter it.

    >>> find('/path/to/filtered.file')
    ('/path/to/filterable.file', <SomeFilter instance>)
    >>> find('/path/to/unfiltered.file')
    (None, None)
    """
    filter = filters.find_by_output_path(output_path)
    if filter:
        for possible_path in filter.possible_input_paths(output_path):
            full_path = finders.find(possible_path)
            if full_path:
                return full_path, filter
    return None, None
