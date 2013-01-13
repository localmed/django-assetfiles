class BaseFilter(object):
    """
    Base class for filters that process files.
    """

    def matches_input(self, intput_path):
        """
        Returns true if the input file should be processed by this filter.

        Args:
            input_path: A file path, relative to the static dir.
        """
        return False

    def matches_output(self, output_path):
        """
        Returns true if the output file would be created by this filter.

        Args:
            output_path: A file path, relative to the static dir.
        """
        return False

    def is_filterable(self, output_path):
        """
        Determines wether to filter the file with the given output path.

        Implement this method if there are certain paths that should not
        be processed by this filter, i.e. they are dependencies.

        Args:
            output_path: A file path, relative to the static dir.
        """
        return True

    def derive_input_paths(self, output_path):
        """Returns possible input paths that would create the given output path.

        Args:
            output_path: A file path, relative to the static dir.
        Returns
            A list of search paths. Can be empty.
        """
        return []

    def derive_output_path(self, input_path):
        """
        Returns the path to the ouput file created with the given input path.

        Args:
            input_path: A file path, relative to the static dir.
        Returns:
            An path to the output file, relative to the static dir.
        """
        return None

    def filter(self, input_path):
        """
        Filters the file with the given input path.

        All filters must implement this method.

        Args:
            input_path: An absolute path to the file to filter.

        Returns:
            The filtered string.
        """
        raise NotImplementedError()
