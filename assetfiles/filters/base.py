class BaseFilter(object):
    """
    Base class for filters that process files.
    """
    # input_path = None
    # output_path = None

    def __init__(self, input_path=None, output_path=None):
        self.input_path = input_path
        self.output_path = output_path

    def matches_input(self, input_path):
        """
        Returns true if the input file should be processed by this filter.

        Args:
            input_path: A file path, relative to the static dir.
        """
        if self.input_path:
            return input_path is self.input_path
        else:
            return self._matches_input(input_path)

    def _matches_input(self, input_path):
        return False

    def matches_output(self, output_path):
        """
        Returns true if the output file would be created by this filter.

        Args:
            output_path: A file path, relative to the static dir.
        """
        if self.output_path:
            return output_path is self.output_path
        else:
            return self._matches_output(output_path)

    def _matches_output(self, input_path):
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
        if self.input_path:
            return [self.input_path]
        else:
            return self._derive_input_paths(output_path)

    def _derive_input_paths(self, output_path):
        return []

    def derive_output_path(self, input_path):
        """
        Returns the path to the ouput file created with the given input path.

        Args:
            input_path: A file path, relative to the static dir.
        Returns:
            An path to the output file, relative to the static dir.
        """
        if self.output_path:
            return self.output_path
        else:
            return self._derive_output_path(input_path)

    def _derive_output_path(self, input_path):
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
