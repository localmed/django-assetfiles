import re


class SingleOutputMixin(object):
    def __init__(self, output_path):
        self.output_path = output_path

    def matches_output(self, output_path):
        return output_path is self.output_path

    def derive_output_path(self, input_path):
        return self.output_path


class SingleInputMixin(object):
    def __init__(self, input_path):
        self.input_path = input_path

    def matches_input(self, input_path):
        return input_path is self.input_path

    def derive_input_paths(self, output_path):
        return [self.input_path]


class GlobInputMixin(object):
    def __init__(self, input_path_glob):
        self.input_path_glob = input_path_glob

    def matches_input(self, input_path):
        from fnmatch import fnmatch

        return fnmatch(input_path, self.input_path_glob)

    def derive_input_paths(self, output_path):
        input_paths = []
        for root in self._get_staticfiles_roots():
            for path in self._iglob_within(root, self.input_path_glob):
                if path not in input_paths:
                    input_paths.append(path)
        return input_paths

    def _iglob_within(self, root, pathname):
        try:
            from glob2 import iglob
        except ImportError:
            from glob import iglob
        import os

        for path in iglob(os.path.join(root, pathname)):
            yield path.replace(root, '').lstrip('/')

    def _get_staticfiles_roots(self):
        for storages in self._get_staticfiles_storages():
            for root, storage in storages.iteritems():
                if hasattr(storage, 'location'):
                    yield storage.location

    def _get_staticfiles_storages(self):
        from django.contrib.staticfiles.finders import get_finders

        for finder in get_finders():
            if hasattr(finder, 'storages'):
                yield finder.storages


class ListInputMixin(object):
    def __init__(self, input_paths):
        self.input_paths = input_paths

    def matches_input(self, input_path):
        return input_path in self.input_paths

    def derive_input_paths(self, output_path):
        return list(self.input_paths)


class MultiInputMixin(object):
    def __init__(self, input_paths):
        if isinstance(input_paths, str):
            self._multi_input_delegate = GlobInputMixin(input_path_glob=input_paths)
        else:
            self._multi_input_delegate = ListInputMixin(input_paths=input_paths)

    def matches_input(self, input_path):
        return self._multi_input_delegate.matches_input(input_path)

    def derive_input_paths(self, output_path):
        return self._multi_input_delegate.derive_input_paths(output_path)


class ExtensionMixin(object):
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

    def derive_input_paths(self, output_path):
        paths = []
        if self.input_exts:
            for ext in self.input_exts:
                ext = '.' + ext
                paths.append(output_path + ext)
                paths.append(re.sub(r'\.[^\.]*$', ext, output_path))
        return paths

    def derive_output_path(self, input_path):
        if self.output_ext:
            path = re.sub(r'\.{0}'.format(self.output_ext), '', input_path)
            ext = '.' + self.output_ext
            return re.sub(r'\.[^\.]*$', ext, path)
        return None

    def set_input_ext(self, value):
        self.input_exts = (value,)
    input_ext = property(fset=set_input_ext)
