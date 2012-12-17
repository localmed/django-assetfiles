import re


class BaseFilter(object):
    """
    Base class for filters that process files.
    """

    def matches_input(self, intput_path):
        """
        Returns true if the input file should be processed by this filter.

        Args:
            input_path: An absolute path to the file
        """
        return False

    def matches_output(self, output_path):
        """
        Returns true if the output file would be created by this filter.

        Args:
            output_path: An absolute path to the file
        """
        return False

    def possible_input_paths(self, output_path):
        """Returns possible input paths that would create the given output path.

        Args:
            output_path: An absolute path to the file
        Returns
            A set of search paths. Can be empty.

        """
        return set()

    def output_path(self, input_path):
        """
        Returns the path to the ouput file created with the given input path.

        Args:
            input_path: An absolute path to the file
        Returns:
            An absolute path to the output file.
        """
        return None

    def skip_output_path(self, output_path):
        """
        Determines wether to filter the file with the given output path.

        Implement this method if there are certain paths that should not
        be processed by this filter, i.e. they are dependencies.

        Args:
            output_path: An absolute path to the file.
        """
        return False

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


class ExtFilter(object):
    """
    A mixin for filters that take a file with a certain file extension and
    output another.

    For example, SassFilter generally takes files with the exentions ".scss" and
    ".sass" and output CSS files (".css").

    Attributes:
        input_exts: A tuple of extensions (without the prefixed ".")
        output_ext: A single output extension (again, without the prefixed ".")
    """
    input_exts = None
    output_ext = None

    def __init__(self):
        if not self.input_exts and self.input_ext:
            self.input_exts = (self.input_ext,)

    def matches_input(self, intput_path):
        if self.input_exts:
            return re.search(r'\.({0})$'.format('|'.join(self.input_exts)), intput_path)
        return False

    def matches_output(self, output_path):
        if self.output_ext:
            return re.search(r'\.{0}$'.format(self.output_ext), output_path)
        return False

    def possible_input_paths(self, output_path):
        paths = set()
        if self.input_exts:
            for ext in self.input_exts:
                ext = '.' + ext
                paths.add(output_path + ext)
                paths.add(re.sub(r'\.[^\.]*$', ext, output_path))
        return paths

    def output_path(self, input_path):
        if self.output_ext:
            path = re.sub(r'\.{0}'.format(self.output_ext), '', input_path)
            ext = '.' + self.output_ext
            return re.sub(r'\.[^\.]*$', ext, path)
        return None

    def set_input_ext(self, value):
        self.input_exts = (value,)
    input_ext = property(fset=set_input_ext)
